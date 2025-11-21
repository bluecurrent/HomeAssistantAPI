"""Data models used for WebSocket payloads in the BlueCurrent API."""

from dataclasses import dataclass
from typing import List


@dataclass
class OverrideCurrentPayload:
    """
    Payload for overriding the charging current on a set of chargepoints.

    Attributes:
        chargepoints (List[str]): List of chargepoint IDs to apply the override to.
        overridestarttime (str): Start time in HH24:MI format.
        overridestartdays (List[str]): Start days using 2-letter weekday codes (e.g., 'MO', 'TU').
        overridestoptime (str): Stop time in HH24:MI format.
        overridestopdays (List[str]): Stop days using 2-letter weekday codes.
        overridevalue (float): Amperes to override the chargepoints with.
    """

    chargepoints: List[str]
    overridestarttime: str
    overridestartdays: List[str]
    overridestoptime: str
    overridestopdays: List[str]
    overridevalue: float


@dataclass
class UpdatePriceBasedSettingsPayload:
    """
    Payload for updating the price based settings.

    Attributes:
        expected_departure_time (str | None): Expected vehicle departure time in HH24:MI format.
        current_battery_percentage (int | None): Current battery charge level as number.
        minimum_percentage (int | None): Minimum required battery percentage before smart charging.
        battery_size_kwh (int | None): Total battery capacity in kilowatt-hours (kWh).
    """

    expected_departure_time: str | None = None
    current_battery_percentage: int | None = None
    minimum_percentage: int | None = None
    battery_size_kwh: int | None = None
