def canonical_int(x: int) -> str:
    return str(int(x))


def canonical_vector(values) -> str:
    return "[" + ",".join(canonical_int(x) for x in values) + "]"


def canonical_matrix(matrix) -> str:
    return "[" + ",".join(canonical_vector(row) for row in matrix) + "]"


def canonical_object(obj) -> str:
    if isinstance(obj, dict):
        parts = []
        for key in sorted(obj):
            parts.append(
                '"' + str(key) + '":' + canonical_object(obj[key])
            )
        return "{" + ",".join(parts) + "}"

    if isinstance(obj, list):
        return "[" + ",".join(canonical_object(x) for x in obj) + "]"

    if isinstance(obj, int):
        return str(obj)

    if isinstance(obj, str):
        return '"' + obj.replace('"', '\\"') + '"'

    if isinstance(obj, bool):
        return "true" if obj else "false"

    if obj is None:
        return "null"

    raise TypeError(f"Unsupported canonical type: {type(obj)}")