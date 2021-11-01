def calculate_usage_from_phases(phases):
    phases = [p for p in phases if p]
    return round(sum(phases) / len(phases))

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
    v1 = message["data"]["voltage 1"]
    v2 = message["data"]["voltage 2"]
    v3 = message["data"]["voltage 3"]

    v_total = calculate_usage_from_phases((v1, v2 ,v3))
    message["data"]["total voltage"] = v_total

    c1 = message["data"]["current 1"]
    c2 = message["data"]["current 2"]
    c3 = message["data"]["current 3"]

    c_total = calculate_usage_from_phases((c1, c2 ,c3))
    message["data"]["total current"] = c_total

    vehicle_status_key =  message["data"]["vehicle_status"]
    message["data"]["vehicle_status"] = get_vehicle_status(vehicle_status_key)

    return message
    