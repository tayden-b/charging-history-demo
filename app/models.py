from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ChargingSession(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(pattern=r"^CHG-\d{4,6}$")
    owner_id: str
    vehicle: str
    charged_at: datetime
    energy_wh: int = Field(ge=0)
    amount_minor: int = Field(ge=0)
    currency: str = "USD"


class ChargingSummary(BaseModel):
    sessions: int
    energy_wh: int
    amount_minor: int
    currency: str = "USD"


class ImportResult(BaseModel):
    imported: int
    session_ids: list[str]
