import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.dexscreener.com/latest"

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "SolixBot/1.0",
}

TIMEOUT = httpx.Timeout(
    timeout=20.0,
    connect=10.0,
)


class DexScreenerAPI:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers=DEFAULT_HEADERS,
            timeout=TIMEOUT,
            follow_redirects=True,
        )

    async def close(self) -> None:
        await self.client.aclose()

    async def _get(self, endpoint: str) -> dict[str, Any]:
        try:
            response = await self.client.get(endpoint)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as exc:
            logger.error(
                "DexScreener HTTP Error %s: %s",
                exc.response.status_code,
                exc.response.text,
            )
            raise

        except httpx.RequestError as exc:
            logger.error("DexScreener Request Error: %s", exc)
            raise

    async def search_pairs(self, query: str) -> list[dict[str, Any]]:
        data = await self._get(f"/dex/search/?q={query}")
        return data.get("pairs", [])

    async def get_token_pairs(
        self,
        token_address: str,
    ) -> list[dict[str, Any]]:
        data = await self._get(
            f"/dex/tokens/{token_address}"
        )
        return data.get("pairs", [])
