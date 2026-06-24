from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Optional

import httpx
from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AnalyticsConfig:
    collector_url: str
    property_id: str
    bearer_token: str
    timeout_seconds: float = 0.5
    ignored_prefixes: tuple[str, ...] = ("/static/", "/assets/", "/admin/", "/setup/", "/config/")
    ignored_paths: set[str] = field(
        default_factory=lambda: {"/health", "/favicon.ico", "/robots.txt", "/sitemap.xml"}
    )


class AnalyticsClient:
    def __init__(self, config: AnalyticsConfig) -> None:
        self.config = config
        self._client = httpx.AsyncClient(timeout=config.timeout_seconds)

    def should_ignore(self, path: str) -> bool:
        return path in self.config.ignored_paths or any(
            path.startswith(prefix) for prefix in self.config.ignored_prefixes
        )

    async def track_request(
        self,
        request: Request,
        response: Response,
        event_name: str = "page_view",
        event_data: Optional[dict[str, Any]] = None,
    ) -> None:
        if self.should_ignore(request.url.path):
            return
        await self.track_event(request, response.status_code, event_name, event_data or {})

    async def track_event(
        self,
        request: Request,
        status_code: int,
        event_name: str,
        event_data: Optional[dict[str, Any]] = None,
    ) -> None:
        payload = {
            "property_id": self.config.property_id,
            "event_name": event_name,
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "request": {
                "method": request.method,
                "scheme": request.url.scheme,
                "host": request.url.hostname or request.headers.get("host", ""),
                "path": request.url.path,
                "query": request.url.query,
                "status_code": status_code,
                "referrer": request.headers.get("referer", ""),
                "user_agent": request.headers.get("user-agent", ""),
                "client_ip": client_ip(request),
                "route_name": route_name(request),
                "request_id": request.headers.get("x-request-id", ""),
            },
            "event_data": event_data or {},
        }
        try:
            await self._client.post(
                f"{self.config.collector_url.rstrip('/')}/v1/events",
                json=payload,
                headers={"Authorization": f"Bearer {self.config.bearer_token}"},
            )
        except Exception as exc:
            logger.warning("website analytics submission failed: %s", exc)


def analytics_client_from_env(property_id: str, token_env: str) -> Optional[AnalyticsClient]:
    collector_url = os.getenv("WEBSITE_ANALYTICS_COLLECTOR_URL", "").strip()
    token = os.getenv(token_env, "").strip()
    if not collector_url or not token:
        return None
    return AnalyticsClient(
        AnalyticsConfig(
            collector_url=collector_url,
            property_id=property_id,
            bearer_token=token,
        )
    )


def install_analytics_middleware(app: Any, client: Optional[AnalyticsClient]) -> None:
    app.state.analytics_client = client
    if client is None:
        return

    @app.middleware("http")
    async def analytics_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)
        if not client.should_ignore(request.url.path):
            asyncio.create_task(client.track_request(request, response))
        return response


async def track_event(
    request: Request,
    event_name: str,
    event_data: Optional[dict[str, Any]] = None,
    status_code: int = 200,
) -> None:
    client = getattr(request.app.state, "analytics_client", None)
    if client is not None:
        await client.track_event(request, status_code, event_name, event_data or {})


def client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()
    return request.client.host if request.client else ""


def route_name(request: Request) -> str:
    route = request.scope.get("route")
    name = getattr(route, "name", "")
    return name or ""
