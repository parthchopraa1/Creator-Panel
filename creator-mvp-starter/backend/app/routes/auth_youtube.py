from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
import urllib.parse, requests, os, json
from ..core.config import settings
from ..services.token_crypto import encrypt_token
from ..db.db import create_user_if_missing, insert_connector

router = APIRouter(prefix="/auth/youtube", tags=["auth-youtube"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

# For MVP, we assume a single demo user email in env (replace with real auth later)
DEMO_USER_EMAIL = os.getenv("DEMO_USER_EMAIL", "demo@example.com")

@router.get("/start")
def start_auth(state: str = "state123"):
    if not (settings.GOOGLE_CLIENT_ID and settings.GOOGLE_REDIRECT_URI and settings.GOOGLE_SCOPES):
        raise HTTPException(status_code=500, detail="Google OAuth env vars missing")
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": settings.GOOGLE_SCOPES,
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "consent",
        "state": state,
    }
    url = GOOGLE_AUTH_URL + "?" + urllib.parse.urlencode(params, safe=" ")
    return RedirectResponse(url)

@router.get("/callback")
def callback(code: str | None = None, error: str | None = None, state: str | None = None):
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    # Exchange code for tokens
    resp = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=30)
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {resp.text}")
    tok = resp.json()
    access = tok.get("access_token")
    refresh = tok.get("refresh_token")  # may be absent if not prompted for consent; ensure prompt=consent
    if not access:
        raise HTTPException(status_code=400, detail="No access token returned")
    # Store encrypted
    access_enc = encrypt_token(access)
    refresh_enc = encrypt_token(refresh) if refresh else None

    # Create demo user and save connector
    create_user_if_missing(DEMO_USER_EMAIL)
    insert_connector(
        user_email=DEMO_USER_EMAIL,
        platform="youtube",
        access_enc=access_enc,
        refresh_enc=refresh_enc,
        scopes_json={"scope": settings.GOOGLE_SCOPES.split()}
    )
    # Redirect to a simple success page (could be your frontend)
    return {"status": "ok", "message": "YouTube connected for demo@example.com"}
