"""Wait for a server to respond with a 200 OK."""
from __future__ import annotations

import sys
import time
from typing import Iterable
from urllib.error import URLError
from urllib.request import urlopen


def wait_for_url(url: str, timeout: int = 30, interval: float = 0.5) -> None:
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=5) as response:
                if response.status == 200:
                    return
                last_error = f"Status {response.status}"
        except URLError as exc:
            last_error = str(exc)
        time.sleep(interval)
    raise TimeoutError(f"Timed out waiting for {url}. Last error: {last_error}")


def main(args: Iterable[str]) -> None:
    if not args:
        raise SystemExit("Usage: python scripts/wait_for_server.py <url>")
    wait_for_url(args[0])


if __name__ == "__main__":
    main(sys.argv[1:])
