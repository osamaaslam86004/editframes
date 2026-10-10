from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import STATIC_DIR
from core.lifespan import lifespan
from core.scheduler import scheduler
from api.v1.router import api, ws

app = FastAPI(title="Production Video Studio with KittenTTS", lifespan=lifespan)

app.mount("/dashboard", StaticFiles(directory=STATIC_DIR, html=True), name="static")

app.include_router(api.router, prefix="/api")
app.include_router(ws.router, prefix="/ws")


@app.get("/")
def root():
    return {
        "message": "KittenTTS Video Studio running. Access dashboard at http://localhost:8000/dashboard"
    }


# Start background cron scheduler
scheduler.start()
