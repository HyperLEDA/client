class APIError(Exception):
    @classmethod
    def from_dict(cls, data: dict) -> "APIError":
        return Exception(f"{data['code']} (code {data['status']}): {data['message']}")
