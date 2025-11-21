import os
import gradio as gr
from dotenv import load_dotenv
from bytedance.seedream import SeedreamClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv()
API_KEY = os.getenv("ARK_API_KEY")
seedream_client = SeedreamClient(API_KEY)

def generate_seedream(prompt, images_text, max_images, size, watermark):
    images = [line.strip() for line in images_text.splitlines() if line.strip()]
    urls = seedream_client.generate_images(
        prompt=prompt,
        images=images,
        max_images=max_images,
        size=size,
        watermark=watermark,
    )
    return urls

# ------------------ GRADIO UI ------------------
gradio_app = gr.Interface(
    fn=generate_seedream,
    inputs=[
        gr.Textbox(label="Prompt", lines=3),
        gr.Textbox(label="Reference Image URLs (optional)", lines=3),
        gr.Slider(1, 6, value=3, step=1, label="Number of Images"),
        gr.Dropdown(["2K", "1K", "512x512"], value="2K", label="Size"),
        gr.Checkbox(label="Watermark", value=True),
    ],
    outputs=gr.Gallery(label="Generated Images", columns=3, height="auto"),
    title="Seedream Image Generator",
)

# ------------------ FASTAPI WRAPPER ------------------
app = FastAPI()

# CORS (important for Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Gradio at root "/"
app = gr.mount_gradio_app(app, gradio_app, path="/")

# DO NOT define your own "/" route — it breaks Gradio!


# ------------------ LOCAL RUN ------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)








