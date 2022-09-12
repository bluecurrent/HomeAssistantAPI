from datetime import datetime


def calculate_usage_from_phases(phases: tuple):
    """Get the average of the phases that are not 0."""
    used_phases = [p for p in phases if p]
    if len(used_phases):
        return round(sum(used_phases) / len(used_phases), 1)
    else:
        return 0


def create_datetime(timestamp: str):
    """Get a datetime object from an timestamp."""
    if timestamp == "":
        return None
    timestamp += "+00:00"
    return datetime.strptime(timestamp, "%Y%m%d %H:%M:%S%z")


def get_vehicle_status(vehicle_status_key: str):
    """Get the vehicle status."""
    statuses = {
        "A": "standby",
        "B": "vehicle detected",
        "C": "ready",
        "D": "with ventialtion",
        "E": "no power",
        "F": "error",
    }

    return statuses[vehicle_status_key]


def handle_status(message: dict):
    """Transform status values and add others."""
    v1 = message["data"]["actual_v1"]
    v2 = message["data"]["actual_v2"]
    v3 = message["data"]["actual_v3"]

    v_total = calculate_usage_from_phases((v1, v2, v3))
    message["data"]["total_voltage"] = v_total

    c1 = message["data"]["actual_p1"]
    c2 = message["data"]["actual_p2"]
    c3 = message["data"]["actual_p3"]

    c_total = calculate_usage_from_phases((c1, c2, c3))
    message["data"]["total_current"] = c_total

    vehicle_status_key = message["data"]["vehicle_status"]
    message["data"]["vehicle_status"] = get_vehicle_status(vehicle_status_key)

    start_datetime = message["data"]["start_datetime"]
    new_start_datetime = create_datetime(start_datetime)

    stop_datetime = message["data"]["stop_datetime"]
    new_stop_datetime = create_datetime(stop_datetime)

    message["data"]["start_datetime"] = new_start_datetime
    message["data"]["stop_datetime"] = new_stop_datetime

    offline_since = message["data"]["offline_since"]
    message["data"]["offline_since"] = create_datetime(offline_since)


def handle_grid(message: dict):
    """Add grid_total_current to a message."""
    c1 = message["data"]["grid_actual_p1"]
    c2 = message["data"]["grid_actual_p2"]
    c3 = message["data"]["grid_actual_p3"]

    c_total = calculate_usage_from_phases((c1, c2, c3))
    message["data"]["grid_total_current"] = c_total
