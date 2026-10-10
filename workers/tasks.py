import asyncio
import httpx
import logging

from playwright.async_api import async_playwright

from core.config import get_settings
from workers.celery_app import celery_app
from services.video_service import cleanup_old_videos, render_product_video_sync

logger = logging.getLogger(__name__)
settings = get_settings()


@celery_app.task(
    bind=True,
    name="app.workers.tasks.generate_weekly_videos_task",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=settings.task_max_retries,
)
def generate_weekly_videos_task(self):
    try:
        print("🧹 Cleaning up old promo videos...")
        cleanup_old_videos()

        print("🌐 Fetching product payload from FakeStore API...")
        with httpx.Client() as client:
            response = client.get("https://fakestoreapi.com/products?limit=3")
            products = response.json()

        # Run async Playwright rendering within the celery sync worker context
        async def run_pipeline():
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"]
                )
                for idx, product in enumerate(products, 1):
                    await render_product_video_sync(
                        product, browser, idx, len(products)
                    )
                await browser.close()

        asyncio.run(run_pipeline())
        print("🎉 All AI Voiceover promo reels generated successfully via Celery!")
        return {"status": "success", "count": len(products)}

    except Exception as exc:
        print(f"❌ PIPELINE ERROR: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
