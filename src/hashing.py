import hashlib
from canonical import canonical_object


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_object(obj) -> str:
    payload = canonical_object(obj).encode("utf-8")
    return sha256_bytes(payload)


def hash_chain(items):
    current = "0" * 64

    for item in items:
        payload = current + canonical_object(item)
        current = sha256_bytes(payload.encode("utf-8"))

    return current