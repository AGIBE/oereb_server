# test_concurrent_requests.py
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class Counts:
    fast: int
    slow: int


def count_objects(response: requests.Response) -> int:
    """Zählt die PLRs im Resultat."""
    response.raise_for_status()
    plr_count = len(
        response.json()["GetExtractByIdResponse"]["extract"]["RealEstate"][
            "RestrictionOnLandownership"
        ]
    )
    return plr_count


def run_extract(session: requests.Session, url: str) -> int:
    """Holt den Auszug und zählt die PLRs"""
    return count_objects(session.get(url))


def sequential_counts(slow_url: str, fast_url: str) -> Counts:
    """Kurzer und langer Request nacheinander."""
    with requests.Session() as s:
        fast = run_extract(s, fast_url)
        slow = run_extract(s, slow_url)
    return Counts(fast=fast, slow=slow)


def parallel_counts(slow_url: str, fast_url: str) -> Counts:
    """Langer Request startet zuerst, der kurze läuft währenddessen."""
    slow_started = threading.Event()

    def long_task() -> int:
        with requests.Session() as s:
            slow_started.set()
            return run_extract(s, slow_url)

    def short_task() -> int:
        # Sicherstellen, dass der lange Request bereits unterwegs ist
        assert slow_started.wait(timeout=10), "Langer Request wurde nicht gestartet"
        with requests.Session() as s:
            return run_extract(s, fast_url)

    with ThreadPoolExecutor(max_workers=2) as pool:
        slow_future = pool.submit(long_task)
        slow_started.wait(timeout=10)
        fast_future = pool.submit(short_task)

        fast = fast_future.result()
        # Der kurze muss fertig sein, während der lange noch läuft
        slow_still_running = not slow_future.done()
        slow = slow_future.result()

    assert slow_still_running, (
        "Der kurze Request wurde erst nach dem langen fertig – "
        "die Requests liefen nicht überlappend."
    )
    return Counts(fast=fast, slow=slow)


def test_parallel_requests_return_same_object_counts(
    running_server_instance: str, egrids_for_concurrent_error: tuple
):
    slow_egrid, fast_egrid = egrids_for_concurrent_error
    slow_extract = f"{running_server_instance}/extract/json?egrid={slow_egrid}&lang=de&geometry=true"
    fast_extract = f"{running_server_instance}/extract/json?egrid={fast_egrid}&lang=de&geometry=true"

    sequential = sequential_counts(slow_extract, fast_extract)
    parallel = parallel_counts(slow_extract, fast_extract)

    assert parallel.fast == sequential.fast, (
        f"Kurzer Request: sequentiell={sequential.fast}, parallel={parallel.fast}"
    )
    assert parallel.slow == sequential.slow, (
        f"Langer Request: sequentiell={sequential.slow}, parallel={parallel.slow}"
    )
