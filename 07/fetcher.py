# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
from __future__ import annotations

import argparse
import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import aiohttp

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)


@dataclass(slots=True)
class FetchResult:
    url: str
    status: int
    bytes_downloaded: int

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.url} {self.status} {self.bytes_downloaded} B"


async def fetch_url(
    session: aiohttp.ClientSession,
    url: str,
    sem: asyncio.Semaphore,
    timeout: int = 15,
) -> FetchResult:
    async with sem:
        try:
            async with session.get(url, timeout=timeout) as resp:
                body = await resp.read()
                logger.debug("Fetched %s (%d)", url, resp.status)
                return FetchResult(url, resp.status, len(body))
        except Exception as exc:  # noqa: BLE001  pylint: disable=broad-except
            logger.error("Error fetching %s: %s", url, exc)
            return FetchResult(url, -1, 0)


async def fetch_all(
    urls: Iterable[str],
    concurrency: int = 5,
) -> list[FetchResult]:
    sem = asyncio.Semaphore(concurrency)
    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(fetch_url(session, u, sem)) for u in urls]
        return await asyncio.gather(*tasks)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Async URL fetcher")
    parser.add_argument(
        "-c",
        "--concurrency",
        type=int,
        default=5,
        help="Число одновременных запросов (default: 5)",
    )
    parser.add_argument(
        "urls_file",
        type=Path,
        help="Путь к файлу со списком URL-ов"
        )
    return parser.parse_args(argv)


def read_urls(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    urls: list[str] = [
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not urls:
        raise ValueError(f"Файл {path} не содержит URL-ов")
    return urls


async def _async_entry(concurrency: int, urls_file: Path) -> None:
    urls = read_urls(urls_file)
    results = await fetch_all(urls, concurrency)
    width = max(map(len, urls))
    for res in results:
        print(
            f"{res.url.ljust(width)}  {res.status:>3}  "
            f"{res.bytes_downloaded:>7} B"
        )


def main(argv: list[str] | None = None) -> None:  # pragma: no cover
    args = parse_args(argv)
    asyncio.run(_async_entry(args.concurrency, args.urls_file))


if __name__ == "__main__":  # pragma: no cover
    main()
