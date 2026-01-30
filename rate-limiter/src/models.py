from dataclasses import dataclass

@dataclass(frozen=True)
class Request:
    user_id: str
    endpoint: str
    timestamp: int   # seconds since epoch (or simulated)
