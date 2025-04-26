import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from spotify_auth import get_spotify_oauth, get_token, set_token_info
from spotify_data import get_top_tracks
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Spotify Listening Habits API"}

@app.get("/login")
def login():
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@app.get("/callback")
def callback(request: Request):
    sp_oauth = get_spotify_oauth()
    code = request.query_params.get("code")

    if code:
        token_info = sp_oauth.get_access_token(code)
        set_token_info(token_info)
        return JSONResponse({"status": "success", "message": "Access token stored!"})
    else:
        return JSONResponse({"status": "error", "message": "No code in callback"}, status_code=400)

@app.get("/api/top-tracks")
def top_tracks():
    access_token = get_token()
    if not access_token:
        return JSONResponse({"status": "error", "message": "Access token missing."}, status_code=401)

    data = get_top_tracks(access_token)
    return JSONResponse({"status": "success", "data": data})
