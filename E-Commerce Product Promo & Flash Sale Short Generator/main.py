import os
import shutil
import subprocess
import asyncio
import httpx
import soundfile as sf  # Added soundfile for reliable audio writing
import sys
import torch
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from playwright.async_api import async_playwright
from apscheduler.schedulers.background import BackgroundScheduler
from huggingface_hub import login
from kokoro import KPipeline


# Load environment variables from .env file
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

try:
    login(token=hf_token)
    print("🔑 Successfully authenticated with Hugging Face Hub.")
except Exception as e:
    print(f"⚠️ Failed to authenticate with Hugging Face Hub: {str(e)}")
    print("   Proceeding without authentication (rate limits may apply).")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_PATH = os.path.join(BASE_DIR, "template.html")

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🐈 Downloading/Checking Kokoro-82M Model (~330 MB)...")
    
    # Pre-download model weights explicitly to guarantee Docker host-cache reuse
    snapshot_download(repo_id="hexgrad/Kokoro-82M")
    
    # Initialize Kokoro KPipeline ('a' = American English)
    models["tts"] = KPipeline(lang_code="a")

    print("🐈 Kokoro-82M Model Loaded Successfully...")

    yield
    models.clear()

# Single FastAPI instance with both title and lifespan
app = FastAPI(
    title="Production Video Studio with KittenTTS", 
    lifespan=lifespan
)

app.mount("/dashboard", StaticFiles(directory=STATIC_DIR, html=True), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()


def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)


def overlay_audio_to_video(video_path: str, audio_path: str, output_path: str):
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "libx264",      # Re-encode WebM/VP8 from Playwright to standard H.264 MP4
        "-pix_fmt", "yuv420p",  # Required for maximum video player compatibility (PotPlayer, VLC, Web browsers)
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    # Allow stderr to be captured so FFmpeg errors show in docker logs if it fails
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"❌ FFmpeg Error: {result.stderr}")

def generate_tts_script(product: dict) -> str:
    title = product.get("title", "")
    price = product.get("price", "")
    return f"Check out this deal! {title}. Now on sale for only {price} dollars. Grab yours today before it sells out!"


def cleanup_old_videos():
    for filename in os.listdir(VIDEOS_DIR):
        file_path = os.path.join(VIDEOS_DIR, filename)
        if os.path.isfile(file_path) and filename.endswith(".mp4"):
            os.remove(file_path)


async def generate_weekly_videos_async():
    try:
        await manager.broadcast("🧹 Cleaning up old promo videos...")
        cleanup_old_videos()

        await manager.broadcast("🌐 Fetching product payload from FakeStore API...")
        async with httpx.AsyncClient() as client:
            response = await client.get("https://fakestoreapi.com/products?limit=3")
            products = response.json()

        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            html_template = f.read()

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

            for idx, product in enumerate(products, 1):
                await manager.broadcast(f"🎙️ [{idx}/{len(products)}] Generating KittenTTS voiceover script...")

                # 1. Generate Voiceover Script
                script_text = generate_tts_script(product)
                wav_path = os.path.join(VIDEOS_DIR, f"voice_{product['id']}.wav")

                # Synthesize audio using Kokoro KPipeline generator
                generator = models["tts"](script_text, voice="af_bella", speed=1.0)
                
                # Kokoro returns generator chunks: (graphemes, phonemes, audio_tensor)
                audio_chunks = []
                for _, _, audio in generator:
                    audio_chunks.append(audio)
                
                # Combine audio chunks and write at 24000Hz standard sample rate
                combined_audio = torch.cat(audio_chunks, dim=0).numpy() if len(audio_chunks) > 1 else audio_chunks[0].numpy()
                sf.write(wav_path, combined_audio, 24000)

                audio_duration = get_audio_duration(wav_path)
                record_duration_ms = int((audio_duration + 1.0) * 1000)

                await manager.broadcast(f"🎬 [{idx}/{len(products)}] Recording video ({audio_duration:.1f}s)...")

                # 3. Inject HTML Template
                rendered_html = html_template \
                    .replace("{{PRODUCT_TITLE}}", product["title"]) \
                    .replace("{{PRICE}}", str(product["price"])) \
                    .replace("{{IMAGE_URL}}", product["image"])

                temp_html_path = os.path.join(BASE_DIR, f"temp_{product['id']}.html")
                with open(temp_html_path, "w", encoding="utf-8") as f:
                    f.write(rendered_html)

                context = await browser.new_context(
                    viewport={"width": 1080, "height": 1920},
                    record_video_dir=VIDEOS_DIR,
                    record_video_size={"width": 1080, "height": 1920}
                )

                page = await context.new_page()
                await page.goto(f"file://{temp_html_path}", wait_until="networkidle")

                # Wait explicitly for images to render
                await page.wait_for_selector("img")

                await page.wait_for_timeout(record_duration_ms)

                await context.close()

                raw_video_path = await page.video.path()

                # 4. Mix KittenTTS WAV + Silent Playwright Video into Final MP4
                final_mp4_path = os.path.join(VIDEOS_DIR, f"product_{product['id']}.mp4")
                overlay_audio_to_video(raw_video_path, wav_path, final_mp4_path)

                # Cleanup temp files
                for pth in [raw_video_path, wav_path, temp_html_path]:
                    if os.path.exists(pth):
                        os.remove(pth)

                await manager.broadcast(f"✅ Created video with voiceover: product_{product['id']}.mp4")

            await browser.close()

        await manager.broadcast("🎉 All AI Voiceover promo reels generated successfully!")

    except Exception as e:
        print(f"❌ PIPELINE ERROR: {str(e)}")
        await manager.broadcast(f"❌ Error during generation: {str(e)}")


def cron_job_wrapper():
    asyncio.run(generate_weekly_videos_async())

scheduler = BackgroundScheduler()
scheduler.add_job(cron_job_wrapper, 'cron', day_of_week='sun', hour=0, minute=0)
scheduler.start()


# --- API ENDPOINTS ---

@app.get("/")
def root():
    return {"message": "KittenTTS Video Studio running. Access dashboard at http://localhost:8000/dashboard"}

@app.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/generate-now")
async def trigger_generation():
    asyncio.create_task(generate_weekly_videos_async())
    return {"status": "started", "message": "KittenTTS generation pipeline started."}

@app.get("/api/videos")
def list_videos():
    files = [f for f in os.listdir(VIDEOS_DIR) if f.endswith(".mp4")]
    return {
        "count": len(files),
        "videos": [
            {
                "filename": filename,
                "download_url": f"/api/videos/download/{filename}"
            }
            for filename in files
        ]
    }

@app.get("/api/videos/download/{filename}")
def download_video(filename: str):
    file_path = os.path.join(VIDEOS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video file not found.")
    
    return FileResponse(path=file_path, filename=filename, media_type="video/mp4")