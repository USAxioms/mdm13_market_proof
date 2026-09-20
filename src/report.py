import json
from hashing import hash_object


def build_report(results):
    report = {
        "capsule": "MDM-WAD18-Scientific-Validation-Capsule",
        "version": "1.0.0",
        "arithmetic": "WAD-18",
        "results": results
    }

    report["report_hash"] = hash_object(report)

    return report


def save_report(report, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)