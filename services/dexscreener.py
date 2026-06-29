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
async def get_trending(self, limit: int = 10):
        """
        Returns the highest-volume pairs from DexScreener boosted tokens.
        """

        try:
            data = await self._request("token-boosts/latest/v1")

            if not isinstance(data, list):
                return []

            filtered = []

            for item in data:
                try:
                    address = item.get("tokenAddress")

                    if not address:
                        continue

                    pairs = await self.token(address)

                    if not pairs:
                        continue

                    pair = pairs[0]

                    volume = (
                        pair.get("volume", {}).get("h24", 0)
                        if pair.get("volume")
                        else 0
                    )

                    liquidity = (
                        pair.get("liquidity", {}).get("usd", 0)
                        if pair.get("liquidity")
                        else 0
                    )

                    filtered.append(
                        {
                            "address": address,
                            "pair": pair,
                            "volume": volume,
                            "liquidity": liquidity,
                        }
                    )

                except Exception as e:
                    logger.warning(f"Skipping token: {e}")

            filtered.sort(
                key=lambda x: (
                    x["volume"],
                    x["liquidity"],
                ),
                reverse=True,
            )

            return filtered[:limit]

        except Exception as e:
            logger.exception(e)
            return []

    async def health_check(self):
        try:
            await self.search("SOL")
            return True
        except Exception:
            return False
