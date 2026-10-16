import csv
import io
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation

from pydantic import ValidationError

from app.models import ChargingSession

MAX_UPLOAD_BYTES = 256 * 1024
MAX_ROWS = 100
CSV_FIELDS = ["session_id", "charged_at", "energy_kwh", "amount_usd"]


def scaled_integer(value: str, scale: int, label: str) -> int:
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{label} must be a decimal number.") from exc
    if not number.is_finite() or number < 0 or number > Decimal("1000000"):
        raise ValueError(f"{label} is outside the accepted range.")
    scaled = number * scale
    if scaled != scaled.to_integral_value():
        raise ValueError(f"{label} has too many decimal places.")
    return int(scaled)


def parse_upload(content: bytes, owner_id: str, vehicle: str) -> list[ChargingSession]:
    if not content or len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("Upload must contain between 1 byte and 256 KiB.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("Upload must be UTF-8 CSV.") from exc
    if "\x00" in text:
        raise ValueError("Upload contains invalid characters.")
    reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
    try:
        if reader.fieldnames != CSV_FIELDS:
            raise ValueError("Columns must be: " + ",".join(CSV_FIELDS))
        rows = []
        for index, record in enumerate(reader, start=2):
            if len(rows) >= MAX_ROWS:
                raise ValueError("Upload must contain no more than 100 records.")
            if None in record or any(value is None for value in record.values()):
                raise ValueError(f"Row {index} has the wrong number of fields.")
            try:
                charged_at = datetime.fromisoformat(record["charged_at"].replace("Z", "+00:00"))
                if charged_at.utcoffset() is None:
                    raise ValueError("charged_at must include a timezone.")
                rows.append(
                    ChargingSession(
                        id=record["session_id"].strip(),
                        owner_id=owner_id,
                        vehicle=vehicle,
                        charged_at=charged_at.astimezone(UTC),
                        energy_wh=scaled_integer(record["energy_kwh"], 1000, "energy_kwh"),
                        amount_minor=scaled_integer(record["amount_usd"], 100, "amount_usd"),
                    )
                )
            except (ValueError, ValidationError) as exc:
                raise ValueError(f"Row {index} is invalid: {exc}") from exc
    except csv.Error as exc:
        raise ValueError("Malformed CSV.") from exc
    if not rows:
        raise ValueError("Upload needs at least one data row.")
    return rows
