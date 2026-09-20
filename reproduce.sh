#!/bin/sh
set -eu

export PYTHONHASHSEED=0

rm -rf results
mkdir -p results

python3 run.py

python3 -m pytest -q tests

echo ""
echo "=========================================="
echo "WAD-18 REPRODUCTION COMPLETE"
echo "=========================================="
echo ""
echo "Normative result:"
echo "results/scientific_verdict.json"