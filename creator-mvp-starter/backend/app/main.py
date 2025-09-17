from fastapi import FastAPI
from .routes import auth_youtube

app = FastAPI(title="Creator MVP API")

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(auth_youtube.router)

@app.get("/me/summary")
def me_summary():
    # TODO: query aggregates; return stub for now
    return {
        "channels": 1,
        "followers": 0,
        "views_30d": 0,
        "est_revenue_30d": 0.0,
        "message": "Connect YouTube via /auth/youtube/start"
    }
