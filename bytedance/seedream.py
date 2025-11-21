import logging
from typing import List, Optional, Dict, Any

from .client import ByteDanceClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SeedreamClient:
    """
    Thin wrapper for the Seedream image generation endpoint.

    Usage:
        client = SeedreamClient(api_key="...")          # raises ValueError if api_key is falsy
        urls = client.generate_images(prompt="...", images=[...])
    """

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
        stream: bool = False,
        response_format: str = "url",
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.MODEL,
            "prompt": prompt,
            "sequential_image_generation": "auto",
            "sequential_image_generation_options": {"max_images": max_images},
            "response_format": response_format,
            "size": size,
            "stream": stream,
            "watermark": watermark,
        }

        # Only include image key if images are provided
        if images:
            payload["image"] = images

        return payload

    def generate_images(
        self,
        prompt: str,
        images: Optional[List[str]] = None,
        max_images: int = 3,
        size: str = "2K",
        watermark: bool = True,
        stream: bool = False,
        response_format: str = "url",
    ) -> List[str]:
        """
        Generate images using Seedream and return a list of URLs (or empty list).

        Notes:
        - `images` should be a list of accessible image URLs (or None).
        - `stream` defaults to False. If you need streaming, handle it separately.
        - `response_format="url"` returns URLs; if using base64 you must decode them.
        """
        payload = self._build_payload(
            prompt=prompt,
            images=images,
            max_images=max_images,
            size=size,
            watermark=watermark,
            stream=stream,
            response_format=response_format,
        )

        logger.info("Calling Seedream with payload keys: %s", list(payload.keys()))
        try:
            result = self.client.post("/images/generations", payload)
        except Exception as e:
            # Bubble up a clearer error message
            logger.exception("Seedream API request failed")
            raise RuntimeError(f"Seedream API request failed: {e}") from e

        # Helpful debug log (avoid printing large content in prod)
        logger.debug("Seedream raw response: %s", result)

        # Normal case: result["data"] is a list of items containing url(s)
        if isinstance(result, dict) and "data" in result and isinstance(result["data"], list):
            urls: List[str] = []
            for item in result["data"]:
                # Try a few likely keys for image URL
                url = None
                if isinstance(item, dict):
                    url = item.get("url") or item.get("output_url") or item.get("image_url")
                # If item itself is a string (some APIs return list of strings)
                if not url and isinstance(item, str):
                    url = item
                if url:
                    urls.append(url)
            return urls

        # If API returned error structure, surface it
        if isinstance(result, dict) and ("error" in result or "message" in result):
            err = result.get("error") or result.get("message")
            raise RuntimeError(f"Seedream API error: {err}")

        # Otherwise return empty and log
        logger.warning("Unexpected Seedream response shape; returning empty list.")
        return []


        result = self.client.post("/images/generations", payload)
        if "data" in result:
            return [item.get("url") for item in result["data"]]
        return []

