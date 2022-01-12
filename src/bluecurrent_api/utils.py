from datetime import datetime


def calculate_usage_from_phases(phases):
    phases = [p for p in phases if p]
    if len(phases):
        return round(sum(phases) / len(phases), 1)
    else:
        return 0


def create_datetime(timestamp):
    if timestamp == "":
        return None
    timestamp += "+02:00"
    return datetime.strptime(timestamp, "%Y%m%d %H:%M:%S%z")


def get_vehicle_status(vehicle_status_key):
    statuses = {
        "A": "standby",
        "B": "vehicle detected",
        "C": "ready",
        "D": "with ventialtion",
        "E": "no power",
        "F": "error",
    }

    return statuses[vehicle_status_key]


def handle_status(message):
    v1 = message["data"]["ch_actual_v1"]
    v2 = message["data"]["ch_actual_v2"]
    v3 = message["data"]["ch_actual_v3"]

    v_total = calculate_usage_from_phases((v1, v2, v3))
    message["data"]["ch_total_voltage"] = v_total

    c1 = message["data"]["ch_actual_p1"]
    c2 = message["data"]["ch_actual_p2"]
    c3 = message["data"]["ch_actual_p3"]

    c_total = calculate_usage_from_phases((c1, c2, c3))
    message["data"]["ch_total_current"] = c_total

    vehicle_status_key = message["data"]["vehicle_status"]
    message["data"]["vehicle_status"] = get_vehicle_status(vehicle_status_key)

    start_datetime = message["data"]["start_datetime"]
    new_start_datetime = create_datetime(start_datetime)

    stop_datetime = message["data"]["stop_datetime"]
    new_stop_datetime = create_datetime(stop_datetime)

    message["data"]["start_datetime"] = new_start_datetime
    message["data"]["stop_datetime"] = new_stop_datetime

    offline_since = message["data"]["ch_offline_since"]
    message["data"]["ch_offline_since"] = create_datetime(offline_since)


def handle_grid(message):
    c1 = message["data"]["grid_actual_p1"]
    c2 = message["data"]["grid_actual_p2"]
    c3 = message["data"]["grid_actual_p3"]

    c_total = calculate_usage_from_phases((c1, c2, c3))
    message["data"]["grid_total_current"] = c_total
