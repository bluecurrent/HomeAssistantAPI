from datetime import datetime


def calculate_usage_from_phases(phases: tuple):
    """Get the average of the phases that are not 0."""
    used_phases = [p for p in phases if p]
    if len(used_phases):
        return round(sum(used_phases) / len(used_phases), 1)
    return 0


def calculate_total_kw(voltage, current):
    """Calculate the total kW"""
    return round((voltage * current / 1000), 2)


def create_datetime(timestamp: str, is_offline_since=False):
    """Get a datetime object from an timestamp."""

    # fix for timezone
    if timestamp == "":
        return None
    # CEST
    timestamp += "+02:00"

    # fix for different formats
    if is_offline_since:
        return datetime.strptime(timestamp, "%Y%m%d %H:%M:%S%z")

    return datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S%z")


def get_vehicle_status(vehicle_status_key: str):
    """Get the vehicle status."""
    statuses = {
        "A": "standby",
        "B": "vehicle_detected",
        "C": "ready",
        "D": "ready",
        "E": "no_power",
        "F": "vehicle_error",
    }

    return statuses[vehicle_status_key]


def handle_status(message: dict):
    """Transform status values and add others."""
    voltage1 = message["data"]["actual_v1"]
    voltage2 = message["data"]["actual_v2"]
    voltage3 = message["data"]["actual_v3"]

    v_total = calculate_usage_from_phases((voltage1, voltage2, voltage3))
    message["data"]["total_voltage"] = v_total

    current1 = message["data"]["actual_p1"]
    current2 = message["data"]["actual_p2"]
    current3 = message["data"]["actual_p3"]

    c_total = calculate_usage_from_phases((current1, current2, current3))
    message["data"]["total_current"] = c_total

    message["data"]["total_kw"] = calculate_total_kw(
        v_total, c_total)

    vehicle_status_key = message["data"]["vehicle_status"]
    message["data"]["vehicle_status"] = get_vehicle_status(vehicle_status_key)

    start_datetime = message["data"]["start_datetime"]
    new_start_datetime = create_datetime(start_datetime)

    stop_datetime = message["data"]["stop_datetime"]
    new_stop_datetime = create_datetime(stop_datetime)

    message["data"]["start_datetime"] = new_start_datetime
    message["data"]["stop_datetime"] = new_stop_datetime

    offline_since = message["data"]["offline_since"]
    message["data"]["offline_since"] = create_datetime(offline_since, True)


def handle_grid(message: dict):
    """Add grid_total_current to a message."""
    current1 = message["data"]["grid_actual_p1"]
    current2 = message["data"]["grid_actual_p2"]
    current3 = message["data"]["grid_actual_p3"]

    c_total = calculate_usage_from_phases((current1, current2, current3))
    message["data"]["grid_total_current"] = c_total


def handle_setting_change(message: dict):
    """Change result to a boolean"""
    message["result"] = "true" in message["result"]["setting"]
    message["object"] = message["object"].replace("STATUS_SET_", "")


def handle_session_messages(message: dict):
    """handle session messages"""

    object_name = message["object"].replace(
        "STATUS_", "").replace("RECEIVED_", "")

    if "STATUS" in message["object"]:
        name = object_name.lower()
        error = message['error'].lower()
        evse_id = message['evse_id']
        message["error"] = f"{name} {error} for chargepoint: {evse_id}"
    message["object"] = object_name
