This file is a merged representation of the entire codebase, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
````
Beginner/
  index.html
  render.py
E-Commerce Product Promo & Flash Sale Short Generator/
  Dockerfile
  main.py
  requirements.txt
  template.html
Intermediate/
  index.html
  render.py
Professional/
  Example_1/
    index.html
    render.py
  Example_2/
    index.html
    render.py
.gitignore
README.md
````

# Files

## File: Beginner/index.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Python Editframe Video</title>
  <!-- Load Editframe Web Components CDN -->
  <script type="module" src="https://cdn.editframe.com/elements/latest/index.js"></script>
  <style>
    body {
      margin: 0;
      background: #0f172a;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      font-family: Arial, sans-serif;
    }
    .title {
      color: #38bdf8;
      font-size: 72px;
      font-weight: bold;
      text-align: center;
      animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.9); }
      to { opacity: 1; transform: scale(1); }
    }
  </style>
</head>
<body>
  <!-- 1080p canvas rendered for 5 seconds -->
  <ef-timegroup mode="fixed" duration="5s" style="width: 1920px; height: 1080px;">
    <div class="title">Hello from Python + HTML/CSS! 🐍🎬</div>
  </ef-timegroup>
</body>
</html>
````

## File: Beginner/render.py
````python
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

        print("🎬 Recording 5 seconds of Beginner video animation...")
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
````

## File: E-Commerce Product Promo & Flash Sale Short Generator/Dockerfile
````dockerfile
# Official Playwright Python image (includes Chromium & OS dependencies)
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for output videos
RUN mkdir -p /app/videos

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start Uvicorn web server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
````

## File: E-Commerce Product Promo & Flash Sale Short Generator/main.py
````python
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
````

## File: E-Commerce Product Promo & Flash Sale Short Generator/requirements.txt
````
fastapi==0.111.0
uvicorn==0.30.1
playwright==1.44.0
httpx==0.27.0
apscheduler==3.10.4
````

## File: E-Commerce Product Promo & Flash Sale Short Generator/template.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Flash Sale Reel</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      width: 1080px;
      height: 1920px;
      background: #090d16;
      overflow: hidden;
      font-family: Arial, sans-serif;
      color: #ffffff;
      padding: 80px 60px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .badge {
      background: #ef4444;
      padding: 20px 40px;
      font-size: 36px;
      font-weight: bold;
      border-radius: 50px;
      align-self: flex-start;
      box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4);
    }
    .img-card {
      width: 960px;
      height: 960px;
      margin: 0 auto;
      border-radius: 40px;
      overflow: hidden;
      background: #ffffff;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .img-card img {
      max-width: 85%;
      max-height: 85%;
      object-fit: contain;
    }
    .details {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .title {
      font-size: 58px;
      font-weight: 800;
      line-height: 1.2;
      color: #f8fafc;
    }
    .price {
      font-size: 80px;
      color: #4ade80;
      font-weight: 900;
    }
    .cta {
      background: linear-gradient(90deg, #6366f1, #8b5cf6);
      padding: 36px;
      text-align: center;
      font-size: 48px;
      font-weight: 800;
      border-radius: 28px;
      text-transform: uppercase;
      box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
    }
  </style>
</head>
<body>
  <div class="badge">⚡ WEEKLY FLASH SALE</div>
  
  <div class="img-card">
    <img src="{{IMAGE_URL}}" alt="Product">
  </div>

  <div class="details">
    <div class="title">{{PRODUCT_TITLE}}</div>
    <div class="price">${{PRICE}}</div>
  </div>

  <div class="cta">SHOP NOW — LINK IN BIO 🛍️</div>
</body>
</html>
````

## File: Intermediate/index.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Intermediate Example - Media Sequencing & Overlays</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      background: #0f172a;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
    }

    /* Video Frame Canvas */
    .stage {
      width: 1920px;
      height: 1080px;
      position: relative;
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    /* Animated Card Component */
    .card {
      background: rgba(30, 41, 59, 0.8);
      border: 2px solid #38bdf8;
      border-radius: 20px;
      padding: 60px 80px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
      text-align: center;
      animation: slideIn 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .badge {
      display: inline-block;
      background: #38bdf8;
      color: #0f172a;
      font-weight: bold;
      font-size: 24px;
      padding: 8px 20px;
      border-radius: 30px;
      text-transform: uppercase;
      margin-bottom: 20px;
      animation: fadeIn 2s ease-in-out;
    }

    .title {
      color: #ffffff;
      font-size: 72px;
      font-weight: 800;
      margin-bottom: 15px;
    }

    .subtitle {
      color: #94a3b8;
      font-size: 36px;
    }

    @keyframes slideIn {
      0% { opacity: 0; transform: translateY(50px) scale(0.95); }
      100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes fadeIn {
      0% { opacity: 0; }
      100% { opacity: 1; }
    }
  </style>
</head>
<body>
  <div class="stage">
    <div class="card">
      <div class="badge">Intermediate Example</div>
      <div class="title">Media Sequencing & Overlays 🎬</div>
      <div class="subtitle">Rendered smoothly with Python + Playwright</div>
    </div>
  </div>
</body>
</html>
````

## File: Intermediate/render.py
````python
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
````

## File: Professional/Example_1/index.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Batch Short Generator</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      width: 1080px;
      height: 1920px;
      background: #000;
      overflow: hidden;
      font-family: Arial, sans-serif;
    }
    .video-canvas {
      width: 1080px;
      height: 1920px;
      position: relative;
      background: #0f172a;
    }
    video {
      width: 100%;
      height: 100%;
      object-fit: cover;
      position: absolute;
      top: 0;
      left: 0;
    }
    .scene {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      display: none;
    }
    .scene.active { display: block; }
    #scene1 { background: linear-gradient(135deg, #1e3a8a, #0f172a); }
    #scene2 { background: linear-gradient(135deg, #065f46, #0f172a); }

    .caption-overlay {
      position: absolute;
      bottom: 150px;
      left: 50px;
      right: 50px;
      background: rgba(0, 0, 0, 0.8);
      color: #ffffff;
      padding: 30px;
      border-radius: 20px;
      font-size: 52px;
      font-weight: bold;
      text-align: center;
      z-index: 10;
      border: 2px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
  </style>
</head>
<body>
  <div class="video-canvas">
    <!-- Scene 1 -->
    <div id="scene1" class="scene active">
      <video id="v1" src="https://assets.editframe.com/departure-prep.mp4" autoplay loop muted playsinline preload="auto"></video>
      <div class="caption-overlay">Scene 1: Departure Prep ✈️</div>
    </div>

    <!-- Scene 2 -->
    <div id="scene2" class="scene">
      <video id="v2" src="https://assets.editframe.com/window-seat.mp4" autoplay loop muted playsinline preload="auto"></video>
      <div class="caption-overlay">Scene 2: Window View 🌥️</div>
    </div>
  </div>

  <script>
    // Sequence switching logic (4 seconds per clip)
    setTimeout(() => {
      document.getElementById('scene1').classList.remove('active');
      const scene2 = document.getElementById('scene2');
      scene2.classList.add('active');
      const v2 = document.getElementById('v2');
      if (v2) v2.play();
    }, 4000);
  </script>
</body>
</html>
````

## File: Professional/Example_1/render.py
````python
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
````

## File: Professional/Example_2/index.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Flash Sale Reel</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      width: 1080px;
      height: 1920px;
      background: #090d16;
      overflow: hidden;
      font-family: 'Montserrat', sans-serif, system-ui;
      color: #ffffff;
    }
    
    .container {
      width: 1080px;
      height: 1920px;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 80px 60px;
      background: radial-gradient(circle at top right, #1e1b4b, #090d16);
    }

    /* Top Flash Sale Badge */
    .header-badge {
      align-self: flex-start;
      background: #ef4444;
      color: #ffffff;
      font-size: 38px;
      font-weight: 900;
      padding: 16px 36px;
      border-radius: 50px;
      text-transform: uppercase;
      letter-spacing: 2px;
      box-shadow: 0 10px 30px rgba(239, 68, 68, 0.5);
      animation: pulse 1.5s infinite alternate;
    }

    /* Product Image Display Card */
    .product-stage {
      width: 960px;
      height: 960px;
      margin: 0 auto;
      border-radius: 40px;
      overflow: hidden;
      position: relative;
      border: 4px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
      animation: zoomIn 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .product-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    /* Price Callout Overlay */
    .price-tag {
      position: absolute;
      bottom: 40px;
      right: 40px;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(12px);
      border: 2px solid #22c55e;
      padding: 20px 40px;
      border-radius: 24px;
      text-align: right;
    }

    .old-price {
      font-size: 36px;
      color: #94a3b8;
      text-decoration: line-through;
    }

    .new-price {
      font-size: 72px;
      font-weight: 900;
      color: #4ade80;
    }

    /* Product Info Section */
    .info-section {
      animation: slideUp 1s ease-out 0.3s backwards;
    }

    .product-title {
      font-size: 64px;
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 20px;
      color: #f8fafc;
    }

    .cta-button {
      width: 100%;
      background: linear-gradient(90deg, #6366f1, #8b5cf6);
      color: #ffffff;
      font-size: 48px;
      font-weight: 800;
      text-align: center;
      padding: 36px;
      border-radius: 28px;
      box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    /* Progress/Timer Bar */
    .timer-bar {
      width: 100%;
      height: 16px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      overflow: hidden;
      margin-top: 40px;
    }

    .timer-progress {
      height: 100%;
      background: #ef4444;
      width: 100%;
      animation: countdown 6s linear forwards;
    }

    /* Keyframe Animations */
    @keyframes pulse {
      0% { transform: scale(1); }
      100% { transform: scale(1.05); }
    }

    @keyframes zoomIn {
      0% { opacity: 0; transform: scale(0.85); }
      100% { opacity: 1; transform: scale(1); }
    }

    @keyframes slideUp {
      0% { opacity: 0; transform: translateY(40px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes countdown {
      0% { width: 100%; }
      100% { width: 0%; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header-badge">⚡ 24-HOUR FLASH SALE</div>

    <div class="product-stage">
      <img class="product-img" src="{{IMAGE_URL}}" alt="Product">
      <div class="price-tag">
        <div class="old-price">{{ORIGINAL_PRICE}}</div>
        <div class="new-price">{{SALE_PRICE}}</div>
      </div>
    </div>

    <div class="info-section">
      <h1 class="product-title">{{PRODUCT_TITLE}}</h1>
      <div class="cta-button">SHOP NOW — LINK IN BIO 🛍️</div>
      <div class="timer-bar">
        <div class="timer-progress"></div>
      </div>
    </div>
  </div>
</body>
</html>
````

## File: Professional/Example_2/render.py
````python
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
````

## File: .gitignore
````
*.mp4

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before launching pyinstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.toml
.cache
.pytest_cache/
.testmondata
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.run/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to share your .python-version.
#   For an app, you may want to ignore it.
#.python-version

# pipenv
#   According to pypa/pipenv#1191, it is recommended to include Pipfile.lock in git.
#   However, in some cases, you might want to change this.
#Pipfile.lock

# poetry
#   With Poetry, standard practice is to commit poetry.lock to git and ignore virtualenvs.
#poetry.lock

# pdm
#   PDM stores project-wide configurations in .pdm.toml
.pdm.toml
.pdm-plugins/

# venv / Virtual Environments (Crucial to ignore)
venv/
.venv/
env/
.env/
ENV/
env.bak/
venv.bak/

# Environment variables and secrets (Never commit secrets!)
.env
.secrets
*.env.local
*.env.*.local

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# OS-specific files (Optional but recommended)
.DS_Store
Thumbs.db

# IDE configurations (VS Code and PyCharm)
.vscode/
.idea/
````

## File: README.md
````markdown
editframes is a Python-based programmatic video generation toolkit designed to demonstrate and implement automated video rendering workflows using Python, HTML templates, and Docker.

### 💡 Key Use Cases
#### Automated Marketing: 
Automated promo generation for daily flash sales or product launches.
#### Serverless Video Pipelines: 
Backend service for generating dynamic social media videos at scale without manual video editing tools.

### 🛠️ Overview of Project Modules
The repository is structured into progressive skill levels, moving from basic script execution to a production-ready containerized microservice:

#### Beginner Level
1. Focus: Simple 
Text Overlay Video.
2. Functionality: 
Demonstrates basic programmatic text rendering onto video backgrounds using Python (render.py).

```
git clone [https://github.com/osamaaslam86004/editframes.git](https://github.com/osamaaslam86004/editframes.git)
cd "Beginner"
python render.py
```

### Intermediate Level
1. Focus: Sequencing Video Clips & Media.
2. Functionality: Handles multi-clip sequencing, transitions, and combining multiple media assets into a single cohesive video output.

```
git clone [https://github.com/osamaaslam86004/editframes.git](https://github.com/osamaaslam86004/editframes.git)
cd "Intermediate"
python render.py
```

### Professional & Scalable Level
1. Focus: Programmatic Batch Generator.
2. Functionality: Scalable batch rendering system (Example_1 and Example_2) designed to automate video production for multiple input datasets at scale.

```
# Example 1
git clone [https://github.com/osamaaslam86004/editframes.git](https://github.com/osamaaslam86004/editframes.git)
cd "Professional/Example_1"
python render.py

# Example 2
git clone [https://github.com/osamaaslam86004/editframes.git](https://github.com/osamaaslam86004/editframes.git)
cd "Professional/Example_2"
python render.py
```

### 🚀 Core Showcase: E-Commerce Video Generator Microservice
For a real-world scenario, let's build an E-Commerce Product Promo & Flash Sale Short Generator (1080x1920 vertical format for Instagram Reels, TikTok, and YouTube Shorts).

In real-world applications, you don't hardcode text into HTML. Instead, a Python script dynamically injects JSON product data (product title, original price, discounted price, timer, and image/video URL) into an HTML template and automatically renders the final video.
### Why this is powerful for Real-World Apps:
Database / API Ready: You can pull thousands of products from a REST API or Postgres DB and feed them directly into PRODUCTS.
#### Zero Manual Editing: 
The script automatically generates high-resolution 1080x1920 vertical MP4s with custom titles, images, and prices.
#### Pure Python Automation: 
Scalable for serverless workers, AWS Lambda, or automated daily cron jobs!
### How to Run It
```
git clone [https://github.com/osamaaslam86004/editframes.git](https://github.com/osamaaslam86004/editframes.git)

cd "E-Commerce Product Promo & Flash Sale Short Generator"

# Build Image
docker build -t video-generator .

# Run Container
docker run -d -p 8000:8000 --name promo-video-service video-generator

# Testing Your Endpoints

1. Trigger Immediate Video Generation
curl -X POST http://localhost:8000/api/generate-now

2. List Newly Generated Videos
curl http://localhost:8000/api/videos

# Response 
{
  "count": 3,
  "videos": [
    {
      "filename": "product_1.mp4",
      "download_url": "/api/videos/download/product_1.mp4"
    },
    {
      "filename": "product_2.mp4",
      "download_url": "/api/videos/download/product_2.mp4"
    }
  ]
}

3. Download Video directly in browser or terminal
http://localhost:8000/api/videos/download/product_1.mp4
```

### Summary
1. Free API: Fetches product details directly from FakeStore API.
2. Cron Job: APScheduler runs inside the container every Sunday to automatically regenerate videos.
3. Auto-Cleanup: cleanup_old_videos() wipes the /videos directory before writing new ones.
4. Rest API: Offers /api/videos and /api/videos/download/{filename} endpoints to download media anywhere.
````
