"""Async LiteLLM client — reusable across builds."""

from __future__ import annotations

import asyncio
from enum import Enum
from typing import AsyncIterator

import litellm
from pydantic import BaseModel, Field

from config import settings


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    role: Role
    content: str


class ContextOverflowError(Exception):
    """Raised when the conversation exceeds the model's context window."""


class LLMResponse(BaseModel):
    content: str
    model: str
    finish_reason: str = ""
    usage: dict = Field(default_factory=dict)


class LLMClient:
    """Thin async wrapper around litellm with retry + timeout."""

    def __init__(
        self,
        model: str = "openai/qwen3.5",
        base_url: str | None = None,
        api_key: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 2048,
        timeout: float = 120.0,
        max_retries: int = 3,
    ):
        base_url = base_url or settings.llm_base_url
        api_key = api_key or settings.llm_api_key
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries

    def _to_dicts(self, messages: list[Message]) -> list[dict]:
        return [{"role": m.role.value, "content": m.content} for m in messages]

    async def _call_with_backoff(self, messages: list[dict], stream: bool = False):
        """Call litellm with exponential backoff on failure."""
        last_err = None
        for attempt in range(self.max_retries):
            try:
                return await litellm.acompletion(
                    model=self.model,
                    messages=messages,
                    api_base=self.base_url,
                    api_key=self.api_key,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout,
                    stream=stream,
                )
            except Exception as e:
                last_err = e
                if attempt < self.max_retries - 1:
                    wait = 2**attempt
                    await asyncio.sleep(wait)
        raise last_err  # type: ignore[misc]

    async def complete(self, messages: list[Message]) -> LLMResponse:
        """Non-streaming completion. Returns full response.

        Raises ContextOverflowError if the conversation exceeds the context window.
        """
        try:
            resp = await self._call_with_backoff(self._to_dicts(messages))
        except Exception as e:
            err_str = str(e).lower()
            if any(k in err_str for k in ("context length", "too many tokens", "maximum context", "context window")):
                raise ContextOverflowError(f"Context overflow: {e}") from e
            raise

        choice = resp.choices[0]
        msg = choice.message
        finish_reason = getattr(choice, "finish_reason", "") or ""
        content = msg.content or ""
        # fallback: thinking models (e.g. Qwen 3.5) put output in reasoning_content
        if not content:
            content = getattr(msg, "reasoning_content", "") or ""
        return LLMResponse(
            content=content,
            model=resp.model,
            finish_reason=finish_reason,
            usage=dict(resp.usage) if resp.usage else {},
        )

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        """Streaming completion. Yields content deltas."""
        resp = await self._call_with_backoff(self._to_dicts(messages), stream=True)
        async for chunk in resp:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
