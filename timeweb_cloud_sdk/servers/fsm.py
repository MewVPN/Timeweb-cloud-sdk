from ..exceptions import ServerError

POWER_ON = "on"
POWER_OFF = "off"

TRANSITIONAL_STATES = {
    "turning_on",
    "turning_off",
    "hard_turning_off",
    "rebooting",
    "hard_rebooting",
    "installing",
    "software_install",
    "reinstalling",
    "cloning",
    "transfer",
    "configuring",
    "removing",
}

TERMINAL_STATES = {
    "removed",
    "blocked",
    "permanent_blocked",
    "no_paid",
}


def ensure_not_terminal(status: str):
    if status in TERMINAL_STATES:
        raise ServerError(f"Server entered terminal state: {status}")


def is_power_on(status: str) -> bool:
    return status == POWER_ON


def is_power_off(status: str) -> bool:
    return status == POWER_OFF


def is_transitioning(status: str) -> bool:
    return status in TRANSITIONAL_STATES
