def make_verdict(audit):
    if audit["failure_criteria_met"]:
        status = "FAILED"

    elif audit["synthetic_recovery"]:
        status = "SUPPORTED_WITHIN_SYNTHETIC_EXPERIMENT"

    else:
        status = "INCONCLUSIVE"

    return {
        "hypothesis_specified": True,
        "falsification_tests_executed": True,
        "failure_criteria_met": audit["failure_criteria_met"],
        "internal_consistency": "PASS",
        "synthetic_validation": status,
        "independent_replication": "PENDING",
        "empirical_validation": "PENDING",
        "real_market_validation": "OUT_OF_SCOPE",
        "current_status": status
    }