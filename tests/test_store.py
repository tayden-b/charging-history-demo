from concurrent.futures import ThreadPoolExecutor

from app.models import ChargingSession
from app.store import SessionConflictError, SessionStore


def test_concurrent_imports_do_not_duplicate_or_overwrite():
    store = SessionStore()
    record = ChargingSession(
        id="CHG-8001",
        owner_id="alice",
        vehicle="Demo vehicle A",
        charged_at="2026-09-19T00:00:00Z",
        energy_wh=1000,
        amount_minor=30,
    )

    def attempt():
        try:
            store.add_many([record])
            return True
        except SessionConflictError:
            return False

    with ThreadPoolExecutor(max_workers=8) as executor:
        outcomes = list(executor.map(lambda _: attempt(), range(20)))
    assert outcomes.count(True) == 1
    assert store.get("CHG-8001") == record
    assert len(store.list_for("alice")) == 3
