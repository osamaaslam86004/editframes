import http.server
import socketserver
import threading
import time
import os
import shutil
from playwright.sync_api import sync_playwright

PORT = 8000
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class DirectoryQuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CURRENT_DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress HTTP server log spam

def start_local_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DirectoryQuietHandler) as httpd:
        httpd.serve_forever()

def record_video():
    print(f"🌐 Starting local server at: http://localhost:{PORT}")
    server_thread = threading.Thread(target=start_local_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    print("🚀 Launching Chromium (vertical 9:16 layout)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--autoplay-policy=no-user-gesture-required",
                "--disable-web-security"  # Prevent CORS blocking of external asset CDN
            ]
        )
        
        # Match 1080x1920 vertical format
        context = browser.new_context(
            viewport={"width": 1080, "height": 1920},
            record_video_dir=CURRENT_DIR,
            record_video_size={"width": 1080, "height": 1920}
        )
        
        page = context.new_page()
        print(f"🌐 Navigating to http://localhost:{PORT}/index.html...")
        page.goto(f"http://localhost:{PORT}/index.html", wait_until="networkidle")

        print("⏳ Buffering media assets...")
        # Gracefully attempt to wait for video data without failing hard on network timeouts
        try:
            page.wait_for_function("""
                () => {
                    const videos = Array.from(document.querySelectorAll('video'));
                    return videos.length === 0 || videos.some(v => v.readyState >= 1);
                }
            """, timeout=5000)
            print("✅ Media streams ready.")
        except Exception:
            print("⚠️ Network delay on remote assets; proceeding with rendering timeline...")

        print("🎬 Recording 8 seconds (2 sequential clips @ 4s each)...")
        time.sleep(8)  # Record full 8-second sequence

        raw_video_path = page.video.path()
        context.close()
        browser.close()

        output_name = os.path.join(CURRENT_DIR, "output.mp4")
        if os.path.exists(raw_video_path):
            if os.path.exists(output_name):
                os.remove(output_name)
            shutil.move(raw_video_path, output_name)
            print(f"✅ SUCCESS! 9:16 Video exported to: {output_name}")
        else:
            print("❌ Error: Video file could not be generated.")

if __name__ == "__main__":
    record_video()