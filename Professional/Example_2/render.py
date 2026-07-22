import http.server
import socketserver
import threading
import time
import os
import shutil
from playwright.sync_api import sync_playwright

PORT = 8000
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Real-world product database payload
PRODUCTS = [
    {
        "id": "prod_01",
        "title": "Wireless Noise-Canceling Headphones",
        "original_price": "$299",
        "sale_price": "$149",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1000&q=80"
    },
    {
        "id": "prod_02",
        "title": "Smart Fitness Watch Series X",
        "original_price": "$199",
        "sale_price": "$89",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=1000&q=80"
    }
]

class DirectoryQuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CURRENT_DIR, **kwargs)

    def log_message(self, format, *args):
        pass

def start_local_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DirectoryQuietHandler) as httpd:
        httpd.serve_forever()

def generate_video_for_product(product, p):
    print(f"\n🎬 Processing Promo Video for: {product['title']}...")

    # 1. Read base template
    with open(os.path.join(CURRENT_DIR, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()

    # 2. Inject product payload into template
    populated_html = html_content \
        .replace("{{PRODUCT_TITLE}}", product["title"]) \
        .replace("{{ORIGINAL_PRICE}}", product["original_price"]) \
        .replace("{{SALE_PRICE}}", product["sale_price"]) \
        .replace("{{IMAGE_URL}}", product["image_url"])

    # 3. Write temporary preview file
    temp_html_path = os.path.join(CURRENT_DIR, "temp_render.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(populated_html)

    # 4. Launch Playwright Headless Browser
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )

    context = browser.new_context(
        viewport={"width": 1080, "height": 1920},
        record_video_dir=CURRENT_DIR,
        record_video_size={"width": 1080, "height": 1920}
    )

    page = context.new_page()
    page.goto(f"http://localhost:{PORT}/temp_render.html", wait_until="networkidle")

    print("⏳ Waiting for product images to load...")
    time.sleep(1)

    print("🎥 Recording 6 seconds of promo video...")
    time.sleep(6)  # Record 6 seconds duration

    raw_video_path = page.video.path()
    context.close()
    browser.close()

    # 5. Save output file
    output_filename = f"promo_{product['id']}.mp4"
    output_path = os.path.join(CURRENT_DIR, output_filename)

    if os.path.exists(raw_video_path):
        if os.path.exists(output_path):
            os.remove(output_path)
        shutil.move(raw_video_path, output_path)
        print(f"✅ SUCCESS! Saved: {output_filename}")

    # Clean up temp html file
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

def batch_render():
    print(f"🌐 Starting background server at: http://localhost:{PORT}")
    server_thread = threading.Thread(target=start_local_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    with sync_playwright() as p:
        for product in PRODUCTS:
            generate_video_for_product(product, p)

    print("\n🎉 ALL PROMO VIDEOS GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    batch_render()