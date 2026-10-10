import asyncio
import httpx
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from playwright.async_api import async_playwright
from config import VIDEOS_DIR
from core.websocket import manager
from services.video_service import cleanup_old_videos, render_product_video

router = APIRouter(
    prefix="/api/v1/videos",
    tags=["Videos"],
    dependencies=[Depends(require_api_key)],
)


async def generate_weekly_videos_async():
    try:
        await manager.broadcast("🧹 Cleaning up old promo videos...")
        cleanup_old_videos()

        await manager.broadcast("🌐 Fetching product payload from FakeStore API...")
        async with httpx.AsyncClient() as client:
            response = await client.get("https://fakestoreapi.com/products?limit=3")
            products = response.json()

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

            for idx, product in enumerate(products, 1):
                await render_product_video(product, browser, idx, len(products))

            await browser.close()

        await manager.broadcast(
            "🎉 All AI Voiceover promo reels generated successfully!"
        )
    except Exception as e:
        print(f"❌ PIPELINE ERROR: {str(e)}")
        await manager.broadcast(f"❌ Error during generation: {str(e)}")


@router.post("/generate")
async def trigger_generation():
    asyncio.create_task(generate_weekly_videos_async())
    return {"status": "started", "message": "KittenTTS generation pipeline started."}


@router.get("/")
def list_videos():
    files = [f for f in os.listdir(VIDEOS_DIR) if f.endswith(".mp4")]
    return {
        "count": len(files),
        "videos": [
            {"filename": filename, "download_url": f"/api/videos/download/{filename}"}
            for filename in files
        ],
    }


@router.get("/videos/download/{filename}")
def download_video(filename: str):
    file_path = os.path.join(VIDEOS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video file not found.")
    return FileResponse(path=file_path, filename=filename, media_type="video/mp4")
