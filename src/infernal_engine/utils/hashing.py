import hashlib
import uuid


def string_to_uuid4(s: str) -> str:
    hash_bytes = hashlib.sha256(s.encode()).digest()[:16]
    return str(uuid.UUID(bytes=hash_bytes))
