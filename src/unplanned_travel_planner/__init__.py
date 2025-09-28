from __future__ import annotations
import os

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
    if os.getenv("PRINT_GEMINI_DEBUG"):
        if os.getenv("GOOGLE_API_KEY"):
            print("[Gemini] GOOGLE_API_KEY loaded from .env (length=*)")
        else:
            print("[Gemini] GOOGLE_API_KEY not found after load_dotenv()")
except Exception:
    # Silently ignore if python-dotenv not installed or fails
    pass

__all__ = []
