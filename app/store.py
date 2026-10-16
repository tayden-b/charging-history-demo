from threading import Lock

from app.models import ChargingSession, ChargingSummary

DEMO_USERS = {"alice": "Alice / Demo vehicle A", "bob": "Bob / Demo vehicle B"}


class SessionConflictError(ValueError):
    pass


class SessionStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._sessions = {
            row.id: row
            for row in [
                ChargingSession(
                    id="CHG-1001",
                    owner_id="alice",
                    vehicle="Demo vehicle A",
                    charged_at="2026-09-10T08:00:00Z",
                    energy_wh=24500,
                    amount_minor=735,
                ),
                ChargingSession(
                    id="CHG-1002",
                    owner_id="alice",
                    vehicle="Demo vehicle A",
                    charged_at="2026-09-12T18:30:00Z",
                    energy_wh=18000,
                    amount_minor=540,
                ),
                ChargingSession(
                    id="CHG-2001",
                    owner_id="bob",
                    vehicle="Demo vehicle B",
                    charged_at="2026-09-11T12:00:00Z",
                    energy_wh=31000,
                    amount_minor=930,
                ),
            ]
        }

    def list_for(self, owner_id: str) -> list[ChargingSession]:
        with self._lock:
            rows = [row for row in self._sessions.values() if row.owner_id == owner_id]
        return sorted(rows, key=lambda row: (row.charged_at, row.id), reverse=True)

    def get(self, session_id: str) -> ChargingSession | None:
        with self._lock:
            return self._sessions.get(session_id)

    def summary_for(self, owner_id: str) -> ChargingSummary:
        rows = self.list_for(owner_id)
        return ChargingSummary(
            sessions=len(rows),
            energy_wh=sum(row.energy_wh for row in rows),
            amount_minor=sum(row.amount_minor for row in rows),
        )

    def add_many(self, rows: list[ChargingSession]) -> None:
        ids = [row.id for row in rows]
        with self._lock:
            if len(ids) != len(set(ids)) or any(key in self._sessions for key in ids):
                raise SessionConflictError("An uploaded session ID already exists or is repeated.")
            self._sessions.update({row.id: row for row in rows})
