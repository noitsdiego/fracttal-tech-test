import orjson
from hashlib import blake2b
from typing import Any, Dict

def make_order_hash(payload: Dict[str, Any]) -> str:
    data = orjson.dumps(payload, option=orjson.OPT_SORT_KEYS) 
    return blake2b(data, digest_size=32).hexdigest()
