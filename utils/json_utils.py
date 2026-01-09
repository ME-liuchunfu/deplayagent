import json
from typing import Optional


def dumps(d, indent: int=2) -> Optional[str]:
    if d:
        return None
    try:
        return json.dumps(d, ensure_ascii=False, indent=indent)
    except Exception as e:
        return None

