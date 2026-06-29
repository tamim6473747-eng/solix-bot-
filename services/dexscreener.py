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
        async def get_pair(
        self,
        chain_id: str,
        pair_address: str,
    ) -> dict[str, Any]:

        data = await self._get(
            f"/dex/pairs/{chain_id}/{pair_address}"
        )

        pairs = data.get("pairs", [])

        if not pairs:
            return {}

        return pairs[0]

    async def get_boosted_tokens(self) -> list[dict[str, Any]]:
        response = await self.client.get(
            "https://api.dexscreener.com/token-boosts/top/v1"
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

        return []

    @staticmethod
    def best_pair(
        pairs: list[dict[str, Any]]
    ) -> dict[str, Any]:

        if not pairs:
            return {}

        return max(
            pairs,
            key=lambda pair: pair.get(
                "liquidity",
                {},
            ).get(
                "usd",
                0,
            ),
        )

    @staticmethod
    def format_number(value: Any) -> str:
        try:
            value = float(value)

            if value >= 1_000_000_000:
                return f"{value/1_000_000_000:.2f}B"

            if value >= 1_000_000:
                return f"{value/1_000_000:.2f}M"

            if value >= 1_000:
                return f"{value/1_000:.2f}K"

            return f"{value:.2f}"

        except Exception:
            return "N/A"
            async def get_trending(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Returns the top boosted tokens with their best trading pair.
        """

        boosted = await self.get_boosted_tokens()

        results = []

        for token in boosted:
            try:
                address = token.get("tokenAddress")

                if not address:
                    continue

                pairs = await self.get_token_pairs(address)

                best = self.best_pair(pairs)

                if not best:
                    continue

                results.append(best)

            except Exception as exc:
                logger.warning(
                    "Failed to process boosted token: %s",
                    exc,
                )

        return results[:limit]


dex_api = DexScreenerAPI()
