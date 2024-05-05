from dataclasses import dataclass


@dataclass
class APIError(Exception):
    code: str
    status: int
    message: str

    @classmethod
    def from_dict(cls, data: dict) -> "APIError":
        return APIError(**data)
