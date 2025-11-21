from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import os
from bytedance.seedream import SeedreamClient
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ARK_API_KEY")
seedream_client = SeedreamClient(API_KEY)

app = FastAPI(title="Seedream Image Generation Service")
templates = Jinja2Templates(directory="templates")

# Removed static mount since we don't have a static/ folder
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "urls": []})

@app.post("/", response_class=HTMLResponse)
def generate(
    request: Request,
    prompt: str = Form(...),
    images_text: str = Form(""),
    max_images: int = Form(3),
    size: str = Form("2K"),
    watermark: str = Form("True")
):
    # Convert multiline image URLs to list
    images = [line.strip() for line in images_text.splitlines() if line.strip()]
    urls = seedream_client.generate_images(
        prompt=prompt,
        images=images,
        max_images=max_images,
        size=size,
        watermark=watermark.lower() == "true"
    )
    return templates.TemplateResponse("index.html", {"request": request, "urls": urls, "prompt": prompt, "images_text": images_text})


