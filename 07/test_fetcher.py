# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name,unused-argument
# pylint: disable=protected-access

from __future__ import annotations
import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
import pytest
import fetcher


@pytest.fixture()
def urls_file(tmp_path: Path) -> Path:
    file_ = tmp_path / "urls.txt"
    file_.write_text("http://example.com\n# comment\n\nhttp://example.org")
    return file_


def test_read_urls(urls_file: Path) -> None:
    assert fetcher.read_urls(urls_file) == [
        "http://example.com",
        "http://example.org",
    ]


def test_parse_args() -> None:
    ns = fetcher.parse_args(["-c", "9", "list.txt"])
    assert ns.concurrency == 9 and ns.urls_file.name == "list.txt"


@pytest.mark.asyncio
async def test_fetch_url_success() -> None:

    resp_mock = SimpleNamespace(
        status=200,
        read=mock.AsyncMock(return_value=b"OK"),  # type: ignore[arg-type]
    )

    get_cm = mock.AsyncMock()           # async-context-manager → resp_mock
    get_cm.__aenter__.return_value = resp_mock
    session_mock = mock.Mock(get=mock.Mock(return_value=get_cm))

    sem = asyncio.Semaphore(1)
    res = await fetcher.fetch_url(session_mock, "http://t", sem)
    assert res.status == 200 and res.bytes_downloaded == 2
    session_mock.get.assert_called_once_with("http://t", timeout=15)


@pytest.mark.asyncio
async def test_fetch_all(monkeypatch: pytest.MonkeyPatch) -> None:

    async def _fake_fetch(_session, url, _sem, _timeout=15):  # noqa: D401
        return fetcher.FetchResult(url, 200, 1)

    monkeypatch.setattr(fetcher, "fetch_url", _fake_fetch)

    urls = [f"http://e{i}.com" for i in range(20)]
    res = await fetcher.fetch_all(urls, concurrency=3)
    assert len(res) == 20 and all(r.status == 200 for r in res)


@pytest.mark.asyncio
async def test_fetch_url_error() -> None:
    session_mock = mock.Mock(get=mock.Mock(side_effect=RuntimeError("fail")))
    sem = asyncio.Semaphore(1)
    res = await fetcher.fetch_url(session_mock, "http://bad", sem)
    assert res.status == -1
    assert res.bytes_downloaded == 0


def test_read_urls_empty(tmp_path: Path) -> None:
    f = tmp_path / "urls.txt"
    f.write_text("# коммент\n\n   # ещё\n")
    with pytest.raises(ValueError):
        fetcher.read_urls(f)


@pytest.mark.asyncio
async def test_async_entry_prints_correctly(
    tmp_path: Path,
    capsys,
    monkeypatch
) -> None:
    fn = tmp_path / "u.txt"
    fn.write_text("u\n")

    async def fake_all(urls, concurrency):
        return [fetcher.FetchResult("u", 7, 13)]
    monkeypatch.setattr(fetcher, "fetch_all", fake_all)

    await fetcher._async_entry(3, fn)
    out = capsys.readouterr().out
    width = len("u")
    expected = f"{'u'.ljust(width)}  {7:>3}  {13:>7} B\n"
    assert out == expected


def test_main_calls_async_entry(monkeypatch) -> None:
    args = SimpleNamespace(concurrency=42, urls_file=Path("f.txt"))
    monkeypatch.setattr(fetcher, "parse_args", lambda argv=None: args)
    called = {}

    async def fake_entry(c, f):
        called["c"] = c
        called["f"] = f
    monkeypatch.setattr(fetcher, "_async_entry", fake_entry)

    def fake_run(coro):
        asyncio.get_event_loop().run_until_complete(coro)
    monkeypatch.setattr(fetcher.asyncio, "run", fake_run)

    fetcher.main([])
    assert called == {"c": 42, "f": Path("f.txt")}


def test_parse_args_default() -> None:
    ns = fetcher.parse_args(["urls.lst"])
    assert ns.concurrency == 5
    assert ns.urls_file.name == "urls.lst"
