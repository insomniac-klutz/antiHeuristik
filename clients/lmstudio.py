"""LMStudio model management client — load, unload, list via REST API.

Uses LMStudio's native v1 API (available since LMStudio 0.4.0).
Endpoints:
  POST /api/v1/models/load      → returns {instance_id, status, load_time_seconds}
  POST /api/v1/models/unload    → takes {instance_id}, returns {instance_id}
  GET  /api/v1/models           → returns {models: [...]} with loaded_instances per model
  GET  /v1/models               → OpenAI compat, all downloaded models
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass

import httpx

from config import settings


@dataclass
class VRAMInfo:
    """GPU VRAM snapshot in MB."""
    total_mb: int
    used_mb: int
    free_mb: int

    @property
    def total_gb(self) -> float:
        return round(self.total_mb / 1024, 2)

    @property
    def used_gb(self) -> float:
        return round(self.used_mb / 1024, 2)

    @property
    def free_gb(self) -> float:
        return round(self.free_mb / 1024, 2)

    def bar(self, width: int = 20) -> str:
        """Compact VRAM bar: [████░░░░] 7.2/12.0GB"""
        ratio = self.used_mb / self.total_mb if self.total_mb else 0
        filled = int(ratio * width)
        return (
            f"[{'█' * filled}{'░' * (width - filled)}] "
            f"{self.used_gb}/{self.total_gb}GB"
        )


def get_vram() -> VRAMInfo | None:
    """Read VRAM from nvidia-smi. Returns None if unavailable."""
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.total,memory.used,memory.free",
             "--format=csv,noheader,nounits"],
            text=True,
            timeout=5,
        ).strip()
        total, used, free = (int(x.strip()) for x in out.split(","))
        return VRAMInfo(total_mb=total, used_mb=used, free_mb=free)
    except Exception:
        return None


class LMStudioManager:
    """Manages model lifecycle on a running LMStudio instance."""

    def __init__(self, base_url: str | None = None, timeout: float = 300.0):
        self.base_url = (base_url or settings.llm_base_url).rstrip("/v1").rstrip("/")
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}/api/v1{path}"

    # ── listing ────────────────────────────────────────────

    def _get_models_raw(self) -> dict:
        """Raw response from GET /api/v1/models."""
        resp = httpx.get(self._url("/models"), timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def list_loaded_instance_ids(self) -> list[str]:
        """Return instance_ids of all currently loaded model instances.

        GET /api/v1/models returns models with a `loaded_instances` array.
        Each loaded instance has an `instance_id`. Models with empty
        loaded_instances are downloaded but not in memory.
        """
        data = self._get_models_raw()
        instance_ids = []

        # response may be {models: [...]} or {data: [...]} depending on version
        models = data.get("models", data.get("data", []))

        for model in models:
            # each model may have loaded_instances array
            instances = model.get("loaded_instances", [])
            for inst in instances:
                iid = inst.get("id", "")
                if iid:
                    instance_ids.append(iid)

            # fallback: if no loaded_instances field but model has an id,
            # this might be an older API format — skip (not loaded)

        return instance_ids

    @staticmethod
    def _ids_match(a: str, b: str) -> bool:
        """Bidirectional substring match — handles UI vs API id differences."""
        a, b = a.lower(), b.lower()
        return a in b or b in a

    def is_model_loaded(self, model: str) -> bool:
        """Check if a model is currently loaded (bidirectional substring match)."""
        ids = self.list_loaded_instance_ids()
        return any(self._ids_match(model, iid) for iid in ids)

    def list_downloaded(self) -> list[str]:
        """Return model paths for all downloaded models.

        Uses the OpenAI-compat GET /v1/models which in LMStudio returns
        all downloaded (not just loaded) models.
        """
        resp = httpx.get(
            f"{self.base_url}/v1/models", timeout=self.timeout
        )
        resp.raise_for_status()
        return [m.get("id", "") for m in resp.json().get("data", [])]

    def check_available(self, model_paths: list[str]) -> dict[str, bool]:
        """Check which models are downloaded. Returns {path: is_available}."""
        downloaded = self.list_downloaded()
        results = {}
        for path in model_paths:
            results[path] = any(
                path.lower() in d.lower() for d in downloaded
            )
        return results

    # ── load ───────────────────────────────────────────────

    def load(
        self,
        model: str,
        context_length: int = 131072,
        flash_attention: bool = True,
        poll_interval: float = 3.0,
        poll_timeout: float = 180.0,
    ) -> str:
        """Load a model into VRAM. Returns the instance_id.

        If the model is already loaded, returns the existing instance_id.
        Otherwise fires the load request and polls until the model appears.
        """
        # skip if already loaded
        for iid in self.list_loaded_instance_ids():
            if self._ids_match(model, iid):
                print(f"  [load] already loaded: {iid}")
                return iid

        payload = {
            "model": model,
            "context_length": context_length,
            "flash_attention": flash_attention,
        }

        start = time.monotonic()

        # try to get the response (contains instance_id)
        try:
            resp = httpx.post(
                self._url("/models/load"),
                json=payload,
                timeout=poll_timeout,
            )
            resp.raise_for_status()
            instance_id = resp.json().get("instance_id", model)
            elapsed = time.monotonic() - start
            vram = get_vram()
            vram_str = f" | VRAM: {vram.bar()}" if vram else ""
            print(f"  [load] loaded: {instance_id} ({elapsed:.1f}s){vram_str}")
            return instance_id
        except httpx.TimeoutException:
            pass  # load took too long, poll instead

        # poll until model appears in loaded list
        elapsed = 0.0
        while elapsed < poll_timeout:
            for iid in self.list_loaded_instance_ids():
                if self._ids_match(model, iid):
                    total = time.monotonic() - start
                    vram = get_vram()
                    vram_str = f" | VRAM: {vram.bar()}" if vram else ""
                    print(f"  [load] loaded: {iid} ({total:.1f}s){vram_str}")
                    return iid
            time.sleep(poll_interval)
            elapsed += poll_interval

        raise TimeoutError(
            f"Model {model} not loaded after {poll_timeout}s"
        )

    # ── unload ─────────────────────────────────────────────

    def unload(self, instance_id: str) -> None:
        """Unload a specific model instance by its instance_id."""
        resp = httpx.post(
            self._url("/models/unload"),
            json={"instance_id": instance_id},
            timeout=30.0,
        )
        resp.raise_for_status()
        vram = get_vram()
        vram_str = f" | VRAM: {vram.bar()}" if vram else ""
        print(f"  [unload] unloaded: {instance_id}{vram_str}")

    def unload_all(self, verify_timeout: float = 30.0) -> int:
        """Unload every loaded model instance. Verifies all gone before returning."""
        instance_ids = self.list_loaded_instance_ids()
        count = len(instance_ids)

        if not instance_ids:
            print("  [unload_all] no models loaded")
            return 0

        print(f"  [unload_all] unloading {count} instance(s): {instance_ids}")
        for iid in instance_ids:
            try:
                self.unload(iid)
            except Exception as e:
                print(f"  [unload_all] failed to unload {iid}: {e}")

        # deterministic verify: poll until no loaded instances remain
        elapsed = 0.0
        while elapsed < verify_timeout:
            remaining = self.list_loaded_instance_ids()
            if not remaining:
                vram = get_vram()
                vram_str = f" | VRAM: {vram.bar()}" if vram else ""
                print(f"  [unload_all] all clear ({count} removed){vram_str}")
                return count
            # retry stragglers
            for iid in remaining:
                try:
                    self.unload(iid)
                except Exception:
                    pass
            time.sleep(2)
            elapsed += 2

        still = self.list_loaded_instance_ids()
        if still:
            raise RuntimeError(
                f"Failed to unload all after {verify_timeout}s. Still loaded: {still}"
            )
        return count
