from datetime import datetime


def calculate_usage_from_phases(phases):
    phases = [p for p in phases if p]
    return round(sum(phases) / len(phases), 1)


def create_datetime(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

# not supported in Home Assistant


def calculate_duration(start, stop=None):
    if not stop:
        stop = datetime.now()

    return stop - start


def get_vehicle_status(vehicle_status_key):
    statuses = {
        "A": "standby",
        "B": "vehicle detected",
        "C": "ready",
        "D":  "with ventialtion",
        "E":  "no power",
        "F":  "error",
    }

    return statuses[vehicle_status_key]


def handle_status(message):
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

    start_session = message["data"]["start_session"]
    new_start_session = create_datetime(start_session)

    stop_session = message["data"]["stop_session"]
    new_stop_session = create_datetime(stop_session)

    message["data"]["start_session"] = new_start_session
    message["data"]["stop_session"] = new_stop_session
    # message["data"]["session_duration"] = calculate_duration(
    #     new_start_session, new_stop_session
    # )

    offline_since = message["data"]["offline_since"]
    message["data"]["offline_since"] = create_datetime(offline_since)


def handle_grid(message):
    c1 = message["data"]["grid_actual_p1"]
    c2 = message["data"]["grid_actual_p2"]
    c3 = message["data"]["grid_actual_p3"]

    c_total = calculate_usage_from_phases((c1, c2, c3))
    message["data"]["grid_total_current"] = c_total
