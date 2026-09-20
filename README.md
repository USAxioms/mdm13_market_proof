# MDM-WAD18 Scientific Validation Capsule

## Purpose

This capsule tests whether a 13-dimensional MDM subspace, a 27-dimensional
structural subspace, and their combined 40-dimensional state can recover
known relationships under deterministic synthetic experiments.

The capsule is designed to determine whether the analysis machinery can:

1. recover known dependence,
2. reject null dependence,
3. distinguish 13-D from 27-D contributions,
4. detect interaction between the subspaces,
5. detect leakage,
6. evaluate metric conditioning,
7. preserve deterministic WAD-18 arithmetic.

## Normative Arithmetic

All normative scalar arithmetic uses WAD-18:

    x = X / 10^18

where X is an exact signed integer.

Floating-point arithmetic is prohibited from determining the scientific verdict.

## Experimental Conditions

Four controlled conditions are generated:

1. NULL
2. 13-D SIGNAL
3. 27-D SIGNAL
4. 13x27 INTERACTION

The target is generated independently from the predictor state.

## Scientific Rule

A successful execution is not equivalent to empirical validation.

The capsule reports:

- mathematical consistency,
- deterministic reproducibility,
- synthetic recovery,
- leakage status,
- falsification status.

Real-world market validation is outside the scope of this capsule.

## Execution

    python3 run.py

## Reproduction

    ./reproduce.sh

The final result is written to:

    results/scientific_verdict.json