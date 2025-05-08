from typing import Any


def clean_dict(d: Any) -> Any:
    """
    Recursively remove keys with None values from the dictionary.
    """
    if isinstance(d, list):
        return [clean_dict(item) for item in d]

    if isinstance(d, dict):
        clean = {}
        for k, v in d.items():
            if isinstance(v, dict):
                nested = clean_dict(v)

                if nested:  # Only add non-empty nested dictionaries
                    clean[k] = nested
            elif v is not None:
                clean[k] = clean_dict(v)
        return clean

    return d
