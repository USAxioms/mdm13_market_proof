def extract_agent(rows):
    return [row["agent"] for row in rows]


def extract_structural(rows):
    return [row["structural"] for row in rows]


def extract_combined(rows):
    return [row["state"] for row in rows]


def extract_target(rows):
    return [row["target"] for row in rows]


def incremental_gain(combined, baseline):
    return combined - baseline