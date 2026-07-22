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