from .client import ByteDanceClient
from typing import List, Optional

class SeedreamClient:
    def __init__(self, api_key: str):
        self.client = ByteDanceClient(api_key)

    def generate_images(
        self,
        prompt: str,
        images: Optional[List[str]] = None,
        max_images: int = 3,
        size: str = "2K",
        watermark: bool = True,
        stream: bool = True
    ) -> List[str]:
        """
        Generate images using Seedream.
        Returns a list of URLs.
        """
        payload = {
            "model": "seedream-4-0-250828",
            "prompt": prompt,
            "image": images or [],
            "sequential_image_generation": "auto",
            "sequential_image_generation_options": {"max_images": max_images},
            "response_format": "url",
            "size": size,
            "stream": stream,
            "watermark": watermark
        }

        result = self.client.post("/images/generations", payload)
        if "data" in result:
            return [item.get("url") for item in result["data"]]
        return []
