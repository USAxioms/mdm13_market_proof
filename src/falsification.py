def evaluate_null(observed, null_max):
    return observed <= null_max


def evaluate_recovery(observed, null_max):
    return observed > null_max


def evaluate_interaction(single_a, single_b, combined):
    return combined > max(single_a, single_b)


def audit(results):
    failures = []

    if not results["deterministic"]:
        failures.append("NON_DETERMINISTIC")

    if results["leakage"]:
        failures.append("TARGET_LEAKAGE")

    if not results["synthetic_recovery"]:
        failures.append("SYNTHETIC_RECOVERY_FAILURE")

    return {
        "failure_criteria_met": bool(failures),
        "failures": failures
    }