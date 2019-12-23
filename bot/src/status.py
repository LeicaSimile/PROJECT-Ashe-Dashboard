from enum import Enum

class CommandStatus(Enum):
    COMPLETED = 0
    FAILED = 1
    CANCELLED = 2
    INVALID_INPUT = 3
