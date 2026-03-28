"""Root config — reads service settings from .env, detects GPU VRAM from nvidia-smi."""

import subprocess
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

load_dotenv(Path(__file__).resolve().parent / ".env")


def _detect_vram_gb() -> float:
    """Read total GPU VRAM in GB from nvidia-smi. Returns 0.0 if unavailable."""
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.total",
             "--format=csv,noheader,nounits"],
            text=True,
            timeout=5,
        ).strip()
        return round(int(out.strip()) / 1024, 2)
    except Exception:
        return 0.0


class Settings(BaseSettings):
    llm_base_url: str = Field(default="http://127.0.0.1:1234/v1")
    llm_api_key: str = Field(default="lm-studio")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def gpu_vram_gb(self) -> float:
        """Total GPU VRAM in GB — auto-detected from nvidia-smi."""
        return _detect_vram_gb()


settings = Settings()
