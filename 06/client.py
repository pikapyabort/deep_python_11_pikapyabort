# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from __future__ import annotations
import argparse
import queue
import socket
import threading


def _send(u: str, host: str, port: int) -> None:
    with socket.create_connection((host, port), timeout=5) as s:
        s.sendall(f"{u}\n".encode())
        print(u, "→", s.recv(8192).decode())


def _worker(q: "queue.Queue[str]", host: str, port: int) -> None:
    while True:
        try:
            u = q.get_nowait()
        except queue.Empty:
            break
        _send(u, host, port)
        q.task_done()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("threads", type=int)
    p.add_argument("file")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=9000)
    a = p.parse_args()

    q: "queue.Queue[str]" = queue.Queue()
    with open(a.file, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                q.put(line.strip())

    for _ in range(a.threads):
        threading.Thread(
            target=_worker, args=(q, a.host, a.port), daemon=True
        ).start()
    q.join()


if __name__ == "__main__":
    main()
