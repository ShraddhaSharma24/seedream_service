import logging
from typing import List, Optional, Dict, Any

from .client import ByteDanceClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SeedreamClient:
    MODEL = "seedream-4-0-250828"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Seedream API key is required (ARK_API_KEY).")
        self.client = ByteDanceClient(api_key)

    def _build_payload(
        self,
        prompt: str,
        images: Optional[List[str]] = None,
        max_images: int = 3,
        size: str = "2K",
        watermark: bool = True,
        stream: bool = True,   # IMPORTANT FIX (ByteDance requires stream=True)
        response_format: str = "url",
    ) -> Dict[str, Any]:

        payload = {
            "model": self.MODEL,
            "prompt": prompt,
            "sequential_image_generation": "auto",
            "sequential_image_generation_options": {"max_images": max_images},
            "response_format": response_format,
            "size": size,
            "stream": stream,
            "watermark": watermark,
        }

        if images:
            payload["image"] = images  # matches cURL sample

        return payload

    def generate_images(
        self,
        prompt: str,
        images: Optional[List[str]] = None,
        max_images: int = 3,
        size: str = "2K",
        watermark: bool = True,
        stream: bool = True,  # IMPORTANT FIX
        response_format: str = "url",
    ) -> List[str]:

        payload = self._build_payload(
            prompt=prompt,
            images=images,
            max_images=max_images,
            size=size,
            watermark=watermark,
            stream=stream,
            response_format=response_format,
        )

        logger.info("Payload sent to Seedream: %s", payload)

        try:
            result = self.client.post("/images/generations", payload)
        except Exception as e:
            logger.exception("Seedream API request failed")
            raise RuntimeError(f"Seedream API request failed: {e}")

        logger.info("Seedream response: %s", result)

        # Expected response:
        # { "data": [ { "url": "..." }, { "url": "..." } ] }
        urls: List[str] = []

        if isinstance(result, dict) and "data" in result:
            for item in result["data"]:
                if isinstance(item, dict) and "url" in item:
                    urls.append(item["url"])

            if urls:
                return urls

        # Handle API error
        if isinstance(result, dict) and ("error" in result or "message" in result):
            raise RuntimeError(f"Seedream API error: {result}")

        logger.warning("Unexpected Seedream response. Returning empty list.")
        return []



