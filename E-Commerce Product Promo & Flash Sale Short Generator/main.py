import os
import shutil
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from playwright.sync_api import sync_playwright
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="Automated Video Generator API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
TEMPLATE_PATH = os.path.join(BASE_DIR, "template.html")

os.makedirs(VIDEOS_DIR, exist_ok=True)

def cleanup_old_videos():
    """Deletes all previously generated videos from disk."""
    print("🧹 Requirement #3: Deleting previous week product videos...")
    for filename in os.listdir(VIDEOS_DIR):
        file_path = os.path.join(VIDEOS_DIR, filename)
        if os.path.isfile(file_path) and filename.endswith(".mp4"):
            os.remove(file_path)
            print(f"🗑️ Removed: {filename}")

def generate_weekly_videos():
    """Fetches API products, cleans old files, and records new videos."""
    print("\n🚀 Starting Video Generation Pipeline...")
    
    # 1. Clean up old videos
    cleanup_old_videos()

    # 2. Fetch fresh products from free API
    print("🌐 Requirement #1: Fetching items from FakeStore API...")
    try:
        response = httpx.get("https://fakestoreapi.com/products?limit=3")
        products = response.json()
    except Exception as e:
        print(f"❌ Failed to fetch products: {e}")
        return

    # 3. Read template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()

    # 4. Launch Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        for product in products:
            print(f"🎬 Processing product ID {product['id']}: {product['title']}")

            # Inject product payload
            rendered_html = html_template \
                .replace("{{PRODUCT_TITLE}}", product["title"]) \
                .replace("{{PRICE}}", str(product["price"])) \
                .replace("{{IMAGE_URL}}", product["image"])

            # Write temporary html
            temp_path = os.path.join(BASE_DIR, "temp.html")
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(rendered_html)

            context = browser.new_context(
                viewport={"width": 1080, "height": 1920},
                record_video_dir=VIDEOS_DIR,
                record_video_size={"width": 1080, "height": 1920}
            )

            page = context.new_page()
            page.goto(f"file://{temp_path}", wait_until="networkidle")

            # Record 5 seconds of video
            page.wait_for_timeout(5000)

            raw_path = page.video.path()
            context.close()

            # Rename to predictable filename
            target_path = os.path.join(VIDEOS_DIR, f"product_{product['id']}.mp4")
            if os.path.exists(target_path):
                os.remove(target_path)
            shutil.move(raw_path, target_path)
            print(f"✅ Created: product_{product['id']}.mp4")

            if os.path.exists(temp_path):
                os.remove(temp_path)

        browser.close()
    print("🎉 Pipeline finished successfully!\n")


# Requirement #2: Weekly Cron Scheduler (Runs every Sunday at midnight)
scheduler = BackgroundScheduler()
scheduler.add_job(generate_weekly_videos, 'cron', day_of_week='sun', hour=0, minute=0)
scheduler.start()


# --- REST ENDPOINTS ---

@app.get("/")
def root():
    return {"message": "Video Generator Container is running."}

@app.post("/api/generate-now")
def trigger_generation():
    """Manual REST trigger to force video generation instantly."""
    generate_weekly_videos()
    return {"status": "success", "message": "Batch video generation complete."}

@app.get("/api/videos")
def list_videos():
    """Requirement #4: REST endpoint to list current week generated videos."""
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
    """Requirement #4: REST endpoint to download a specific video."""
    file_path = os.path.join(VIDEOS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video file not found.")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="video/mp4"
    )