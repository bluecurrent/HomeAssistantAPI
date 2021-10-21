def calculate_usage_from_phases(phases):
    phases = [p for p in phases if p]
    return int(sum(phases) / len(phases))

def calculate_watt(v, a):
    return int(v * a)

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

    wh = calculate_watt(v_total, c_total)
    message["data"]["total wh"] = wh

    return message
    