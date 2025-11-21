import gradio as gr
from bytedance.seedream import SeedreamClient
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ARK_API_KEY")
seedream_client = SeedreamClient(API_KEY)

def generate_seedream(prompt, images_text, max_images, size, watermark):
    # Convert multiline text → list
    images = [line.strip() for line in images_text.splitlines() if line.strip()]

    urls = seedream_client.generate_images(
        prompt=prompt,
        images=images,
        max_images=max_images,
        size=size,
        watermark=watermark,
    )

    return urls

# --- Gradio UI ---
app = gr.Interface(
    fn=generate_seedream,
    inputs=[
        gr.Textbox(label="Prompt", placeholder="Describe the image you want...", lines=3),
        gr.Textbox(label="Reference Image URLs (optional)", lines=3),
        gr.Slider(1, 6, value=3, step=1, label="Number of Images"),
        gr.Dropdown(["2K", "1K", "512x512"], value="2K", label="Size"),
        gr.Checkbox(label="Watermark", value=True),
    ],
    outputs=gr.Gallery(label="Generated Images").style(grid=3, height="auto"),
    title="Seedream Image Generator",
    description="Generate stunning AI images with Seedream using your prompts and reference images.",
)

# For Render deployment
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

fastapi_app = FastAPI()
fastapi_app = gr.mount_gradio_app(fastapi_app, app, path="/")

@fastapi_app.get("/")
def home():
    return {"message": "Seedream Gradio App Running"}

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=10000)




