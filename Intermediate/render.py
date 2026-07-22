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
        pass  # Suppress HTTP server output

def start_local_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DirectoryQuietHandler) as httpd:
        httpd.serve_forever()

def record_video():
    print(f"🌐 Starting local server at: http://localhost:{PORT}")
    server_thread = threading.Thread(target=start_local_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    print("🚀 Launching Chromium recorder...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=CURRENT_DIR
        )
        
        page = context.new_page()
        print(f"🌐 Navigating to http://localhost:{PORT}/index.html...")
        page.goto(f"http://localhost:{PORT}/index.html", wait_until="domcontentloaded")

        print("🎬 Recording 5 seconds of Intermediate video animation...")
        time.sleep(5)  # Capture 5 seconds of video

        raw_video_path = page.video.path()
        context.close()
        browser.close()

        output_name = os.path.join(CURRENT_DIR, "output.mp4")
        if os.path.exists(raw_video_path):
            if os.path.exists(output_name):
                os.remove(output_name)
            shutil.move(raw_video_path, output_name)
            print(f"✅ SUCCESS! Video exported to: {output_name}")
        else:
            print("❌ Error: Video file could not be generated.")

if __name__ == "__main__":
    record_video()