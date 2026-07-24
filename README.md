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
3. Auto-Cleanup: wipes the /videos directory before writing new ones.
4. Rest API: Offers /api/videos and /api/videos/download/{filename} endpoints to download media anywhere.
5. Added audio overlay using [Kokoro TTS model](https://github.com/hexgrad/kokoro.git)

#### Convert Repo to .md for Model Training
`npx repomix --remote https://github.com/osamaaslam86004/editframes.git --style markdown`

