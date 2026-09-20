"""
WAD-18 Stress Telemetry
=======================

Combines independently measured quantities.

This module observes mathematical stress.
It does NOT predict crashes.
"""

from wad18 import add, sub, mul, div


NORMAL = "NORMAL"
WATCH = "WATCH"
DIVERGENT = "DIVERGENT"
COLLAPSED = "COLLAPSED"
UNDECIDABLE = "UNDECIDABLE"


def compute_utilization(growth, capacity, epsilon):
    denominator = add(capacity, epsilon)

    if denominator <= 0:
        raise ValueError("Invalid capacity denominator")

    return div(growth, denominator)


def compute_growth_strain(agent_utilization, structural_utilization):
    return sub(agent_utilization, structural_utilization)


def classify_stress(
    rho_state,
    growth_strain,
    strain_threshold,
    gradient_norm,
    gradient_threshold,
    lambda_min,
    metric_floor,
):
    """
    Mathematical observation classifier.

    No future market outcome is referenced.
    """
    if rho_state == UNDECIDABLE:
        return UNDECIDABLE

    divergence = growth_strain >= strain_threshold
    gradient_stress = gradient_norm >= gradient_threshold
    metric_stress = lambda_min <= metric_floor

    if rho_state == COLLAPSED and (divergence or gradient_stress or metric_stress):
        return COLLAPSED

    if divergence or gradient_stress or metric_stress:
        return DIVERGENT

    if rho_state == WATCH:
        return WATCH

    return NORMAL


def build_telemetry(
    time_index,
    agent_growth,
    structural_growth,
    growth_ratio_value,
    growth_difference_value,
    rho_low,
    rho_high,
    rho_state,
    volatility,
    lambda_min,
    lambda_max,
    metric_deformation,
    gradient_norm,
    growth_strain,
    stress_state,
):
    """
    Create deterministic telemetry record.

    All numerical values must already be WAD integers.
    """
    return {
        "time_index": time_index,
        "agent_growth": agent_growth,
        "structural_growth": structural_growth,
        "growth_ratio": growth_ratio_value,
        "growth_difference": growth_difference_value,
        "rho_growth_low": rho_low,
        "rho_growth_high": rho_high,
        "rho_growth_state": rho_state,
        "volatility": volatility,
        "lambda_min": lambda_min,
        "lambda_max": lambda_max,
        "metric_deformation": metric_deformation,
        "gradient_norm": gradient_norm,
        "growth_strain": growth_strain,
        "stress_state": stress_state,
    }
