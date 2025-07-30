from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from auth import build_auth_url, get_token_by_auth_code
from embed import get_embed_info

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Mount the static folder to serve files like /static/powerbi.min.js
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/auth/login")
def login_redirect():
    auth_url = build_auth_url()
    return RedirectResponse(auth_url)


@app.get("/auth/callback")
def callback(code: str, request: Request):
    token = get_token_by_auth_code(code)

    if "access_token" not in token:
        return RedirectResponse(
            "/auth/login"
        )  # Redirect to login if token acquisition fails
    access_token = token["access_token"]
    embed_info = get_embed_info(access_token)

    return templates.TemplateResponse(
        "report_embed.html",
        {
            "request": request,  # ✅ REQUIRED
            "embed_token": access_token,
            "embed_url": embed_info["embedUrl"],
            "report_id": embed_info["id"],
        },
    )
