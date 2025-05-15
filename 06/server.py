# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=broad-exception-caught
from __future__ import annotations
import argparse
import json
import queue
import re
import socket
import threading
from collections import Counter
from contextlib import closing
from typing import Final, NamedTuple
import urllib.request as _request


WORD_RE: Final = re.compile(r"\w+")


def top_k(t: str, k: int) -> dict[str, int]:
    return dict(Counter(WORD_RE.findall(t.lower())).most_common(k))


class Job(NamedTuple):
    sock: socket.socket
    k: int


class Server:  # pylint: disable=too-few-public-methods
    def __init__(self, host: str, port: int, w: int, k: int) -> None:
        self.addr = (host, port)
        self._w = w
        self._k = k
        self._q: queue.Queue[Job] = queue.Queue()
        self._done = 0
        self._lock = threading.Lock()

    def master(self) -> None:
        for _ in range(self._w):
            threading.Thread(target=self.worker, daemon=True).start()

        with closing(socket.socket()) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(self.addr)
            s.listen()
            print(f"[master] listen on {self.addr!r}, workers={self._w}")
            while True:
                c, _ = s.accept()
                self._q.put(Job(c, self._k))

    def worker(self) -> None:
        while True:
            job = self._q.get()
            with closing(job.sock) as s:
                try:
                    u = s.recv(4096).decode().strip()
                    html = fetch(u)
                    s.sendall(json.dumps(top_k(html, job.k)).encode())
                except Exception as e:          # ← теперь перехватываем всё
                    s.sendall(json.dumps({"error": str(e)}).encode())
                finally:
                    with self._lock:
                        self._done += 1
                        print(f"[stat] processed = {self._done}")


def fetch(url: str) -> str:
    with _request.urlopen(url, timeout=10) as r:
        return r.read().decode(errors="ignore")


def _parse_cli() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("-w", "--workers", type=int, default=4)
    p.add_argument("-k", "--top_k", type=int, default=5)
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=9000)
    return p.parse_args()


def main() -> None:
    ns = _parse_cli()
    Server(ns.host, ns.port, ns.workers, ns.top_k).master()


if __name__ == "__main__":
    main()
