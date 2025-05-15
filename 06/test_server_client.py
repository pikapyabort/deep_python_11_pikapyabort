# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=protected-access
from __future__ import annotations
import json
import sys
import types
from contextlib import contextmanager
from typing import Callable
from unittest import mock
from urllib import request
import client
import server


class Msock:
    def __init__(self, recv_data: bytes = b"") -> None:
        self._recv = recv_data
        self.sent: list[bytes] = []
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.closed = True

    def sendall(self, data: bytes) -> None:
        self.sent.append(data)

    def recv(self, _n: int) -> bytes:
        data, self._recv = self._recv, b""
        return data

    def close(self) -> None:
        self.closed = True


@contextmanager
def s_conn(recv_data: bytes = b'{"ok": 1}\n'):
    s = Msock(recv_data)
    with mock.patch("socket.create_connection", return_value=s):
        yield s


def test_client_send_print(capsys):
    with s_conn() as sock:
        client._send("http://x", "127.0.0.1", 9000)
    assert sock.sent[0].endswith(b"\n")
    out = capsys.readouterr().out
    assert "http://x" in out and '{"ok": 1}' in out


def test_client_main(monkeypatch, tmp_path, capsys):
    fp = tmp_path / "u.txt"
    fp.write_text("u1\nu2\n", encoding="utf-8")
    seen: list[str] = []

    def _fake(url: str, *_):
        seen.append(url)

    monkeypatch.setattr(client, "_send", _fake)

    def _run_now(target: Callable, args: tuple, **_):
        target(*args)
        return types.SimpleNamespace(start=lambda: None)

    monkeypatch.setattr(client.threading, "Thread", _run_now)
    monkeypatch.setattr(sys, "argv", ["client.py", "3", str(fp)])

    client.main()
    assert seen == ["u1", "u2"]
    assert not capsys.readouterr().out


def test_top_k():
    assert server.top_k("a b b c c c", 2) == {"c": 3, "b": 2}


def _run_worker_once(html_or_exc):
    srv = server.Server("127.0.0.1", 0, 0, 2)  # type: ignore[arg-type]
    sock = Msock(b"http://x\n")
    job = server.Job(sock, 2)

    done = False

    def fake_get(*_a, **_kw):
        nonlocal done
        if not done:
            done = True
            return job
        raise KeyboardInterrupt

    srv._q.get = fake_get  # type: ignore[method-assign]

    orig_fetch = server.fetch
    if isinstance(html_or_exc, Exception):
        def boom(*_a, **_kw):
            raise html_or_exc
        server.fetch = boom  # type: ignore[assignment]
    else:
        server.fetch = (  # type: ignore[assignment]
            lambda *_a, **_kw: html_or_exc
        )

    try:
        srv.worker()
    except KeyboardInterrupt:
        pass
    finally:
        server.fetch = orig_fetch

    return sock


def test_server_worker_ok():
    sock = _run_worker_once("spam spam eggs")
    assert json.loads(sock.sent[0]) == {"spam": 2, "eggs": 1} and sock.closed


def test_server_worker_err():
    sock = _run_worker_once(RuntimeError("boom"))
    assert json.loads(sock.sent[0])["error"] == "boom" and sock.closed


def test_fetch(monkeypatch):
    class R:  # pylint: disable=too-few-public-methods
        def __enter__(self):
            return self

        def __exit__(self, *_):
            pass

        def read(self):
            return b"abc"

    def _factory(*_a, **_kw):
        return R()

    monkeypatch.setattr(request, "urlopen", _factory)
    assert server.fetch("x") == "abc"


def test_master_accept(monkeypatch):
    srv = server.Server("127.0.0.1", 0, 0, 1)  # type: ignore[arg-type]
    dm = Msock()

    class Sock:  # pylint: disable=too-few-public-methods
        def __init__(self):
            self.once = True

        def setsockopt(self, *_a, **_kw):
            pass

        def bind(self, *_a, **_kw):
            pass

        def listen(self, *_a, **_kw):
            pass

        def accept(self):
            if self.once:
                self.once = False
                return dm, ("peer", 0)
            raise KeyboardInterrupt

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_):
            pass

    def _sock_factory():
        return Sock()

    monkeypatch.setattr(server.socket, "socket", _sock_factory)
    captured: list[server.Job] = []

    def _capture(job: server.Job):
        captured.append(job)
        raise KeyboardInterrupt

    monkeypatch.setattr(srv._q, "put", _capture)  # type: ignore[arg-type]

    try:
        srv.master()
    except KeyboardInterrupt:
        pass

    assert captured and captured[0].sock is dm
