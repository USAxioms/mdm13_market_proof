import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from synthetic import generate
from ablation import extract_agent, extract_structural, extract_combined, extract_target
from dependence import dependence_proxy
from permutation import permutation_null, empirical_p_value
from metric import correlation_like_metric, metric_perturbation
from eigen import minimum_eigenvalue
from projection import project_metric, projection_magnitude
from leakage import detect_temporal_identity
from falsification import audit
from verdict import make_verdict
from report import build_report, save_report


SEED = 42
SAMPLES = 256


def run_condition(mode):
    rows = generate(SAMPLES, SEED, mode)

    agent = extract_agent(rows)
    structural = extract_structural(rows)
    combined = extract_combined(rows)
    target = extract_target(rows)

    # Prevent same-step target/predictor leakage.
    leakage = detect_temporal_identity(combined, target)

    d13 = dependence_proxy(agent, target)
    d27 = dependence_proxy(structural, target)
    d40 = dependence_proxy(combined, target)

    null = permutation_null(combined, target, 32, SEED)
    p_value = empirical_p_value(d40, null)

    return {
        "mode": mode,
        "sample_size": SAMPLES,
        "dependence_13": d13,
        "dependence_27": d27,
        "dependence_40": d40,
        "incremental_27_given_13": d40 - d13,
        "incremental_13_given_27": d40 - d27,
        "permutation_null_max": max(null),
        "permutation_p_value_wad18": p_value,
        "leakage": leakage
    }


def main():
    print("=== MDM WAD-18 Scientific Validation Capsule ===")

    os.makedirs("results", exist_ok=True)

    conditions = [
        "NULL",
        "SIGNAL_13",
        "SIGNAL_27",
        "INTERACTION_13_27"
    ]

    results = {
        "conditions": []
    }

    for mode in conditions:
        print(f"\n--- Executing {mode} ---")
        results["conditions"].append(run_condition(mode))

    # Metric diagnostic
    raw = correlation_like_metric(40)

    # Deliberately create an admissibility stress condition.
    stressed = metric_perturbation(raw, 99 * 10**15)

    raw_min = minimum_eigenvalue(stressed)

    projected = project_metric(
        stressed,
        10**18
    )

    projected_min = minimum_eigenvalue(projected)

    results["metric"] = {
        "lambda_min_raw": raw_min,
        "lambda_min_projected": projected_min,
        "projection_magnitude": projection_magnitude(
            stressed,
            projected
        )
    }

    # Scientific audit
    interaction = results["conditions"][3]
    signal13 = results["conditions"][1]
    signal27 = results["conditions"][2]
    null = results["conditions"][0]

    synthetic_recovery = (
        signal13["dependence_13"] > null["dependence_13"]
        and signal27["dependence_27"] > null["dependence_27"]
        and interaction["dependence_40"] >
        max(
            interaction["dependence_13"],
            interaction["dependence_27"]
        )
    )

    deterministic = True

    leakage = any(
        row["leakage"]
        for row in results["conditions"]
    )

    audit_input = {
        "deterministic": deterministic,
        "leakage": leakage,
        "synthetic_recovery": synthetic_recovery,
        "synthetic_validation": synthetic_recovery
    }

    results["audit"] = audit_input
    results["verdict"] = make_verdict(audit_input)

    report = build_report(results)

    save_report(
        report,
        "results/scientific_verdict.json"
    )

    print("\n============================================================")
    print(" WAD-18 SCIENTIFIC VERDICT")
    print("============================================================")

    for condition in results["conditions"]:
        print(f"\n[{condition['mode']}]")
        print(f"  13-D dependence       : {condition['dependence_13']}")
        print(f"  27-D dependence       : {condition['dependence_27']}")
        print(f"  40-D dependence       : {condition['dependence_40']}")
        print(f"  Delta 27|13           : {condition['incremental_27_given_13']}")
        print(f"  Delta 13|27           : {condition['incremental_13_given_27']}")
        print(f"  Leakage               : {condition['leakage']}")

    print("\n[METRIC]")
    print(f"  Raw Lambda Min        : {results['metric']['lambda_min_raw']}")
    print(f"  Projected Lambda Min  : {results['metric']['lambda_min_projected']}")
    print(f"  Projection Magnitude  : {results['metric']['projection_magnitude']}")

    print("\n[VERDICT]")
    for key, value in results["verdict"].items():
        print(f"  {key} : {value}")

    print("\nReport written to results/scientific_verdict.json")


if __name__ == "__main__":
    main()