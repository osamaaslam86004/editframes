ENV NO_NNPACK=1

FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

# Install system dependencies (FFmpeg for video/audio mixing, eSpeak NG for KittenTTS phonemes)
RUN apt-get update && apt-get install -y ffmpeg espeak-ng && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy English model for text preprocessing in KittenTTS
RUN python -m spacy download en_core_web_sm

COPY . .

RUN mkdir -p /app/videos /app/static

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]