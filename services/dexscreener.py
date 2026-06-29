import httpx
import logging
from typing import Any

from config import DEXSCREENER_BASE_URL

logger = logging.getLogger(__name__)

TIMEOUT = httpx.Timeout(
    connect=10.0,
    read=20.0,
    write=20.0,
    pool=20.0,
)

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "SolixBot/1.0"
}


class DexScreenerAPI:
    def __init__(self):
        self.base_url = DEXSCREENER_BASE_URL

    async def _request(self, endpoint: str) -> Any:
        url = f"{self.base_url}/{endpoint}"

        async with httpx.AsyncClient(
            timeout=TIMEOUT,
            headers=HEADERS,
            follow_redirects=True,
        ) as client:
            response = await client.get(url)

            response.raise_for_status()

            return response.json()

    async def search(self, query: str):
        data = await self._request(
            f"dex/search/?q={query}"
        )

        return data.get("pairs", [])

    async def token(self, address: str):
        data = await self._request(
            f"dex/tokens/{address}"
        )

        return data.get("pairs", [])

    async def latest_pairs(self, chain: str, pair: str):
        return await self._request(
            f"dex/pairs/{chain}/{pair}"
        )


dex_api = DexScreenerAPI()
