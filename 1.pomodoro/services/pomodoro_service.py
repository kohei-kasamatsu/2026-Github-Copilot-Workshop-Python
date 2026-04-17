def get_initial_settings(config: dict) -> dict:
    return {
        "workDurationMinutes": config["WORK_DURATION_MINUTES"],
        "shortBreakMinutes": config["SHORT_BREAK_MINUTES"],
        "longBreakMinutes": config["LONG_BREAK_MINUTES"],
        "longBreakInterval": config["LONG_BREAK_INTERVAL"],
    }