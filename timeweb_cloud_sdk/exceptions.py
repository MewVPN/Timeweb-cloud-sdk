class TimewebError(Exception):
    pass


class AuthenticationError(TimewebError):
    pass


class NotFoundError(TimewebError):
    pass


class ValidationError(TimewebError):
    pass


class RateLimitError(TimewebError):
    pass


class ServerError(TimewebError):
    pass


class TimeoutError(TimewebError):
    pass


class InvalidStateTransition(TimewebError):
    pass
