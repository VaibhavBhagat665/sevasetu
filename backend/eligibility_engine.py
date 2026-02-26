"""
SevaSetu — Rule-Based Eligibility Engine
Deterministic validation of user profiles against scheme rules.
All decisions are explainable with human-readable reasons.
"""

from schemes_data import get_scheme_by_id, get_all_schemes


def _evaluate_rule(rule: dict, user_profile: dict) -> dict:
    """Evaluate a single rule against user profile."""
    field = rule["field"]
    operator = rule["operator"]
    expected = rule["value"]
    label = rule.get("label", f"{field} {operator} {expected}")

    actual = user_profile.get(field)

    # If field not provided, mark as unknown
    if actual is None:
        return {
            "field": field,
            "rule": label,
            "status": "unknown",
            "message": f"Information about '{field}' was not provided. Please provide this detail.",
            "required_value": str(expected),
            "actual_value": None,
        }

    # Evaluate based on operator
    passed = False
    if operator == "eq":
        passed = actual == expected
    elif operator == "neq":
        passed = actual != expected
    elif operator == "gt":
        passed = float(actual) > float(expected)
    elif operator == "gte":
        passed = float(actual) >= float(expected)
    elif operator == "lt":
        passed = float(actual) < float(expected)
    elif operator == "lte":
        passed = float(actual) <= float(expected)
    elif operator == "in":
        passed = actual in expected
    elif operator == "not_in":
        passed = actual not in expected

    return {
        "field": field,
        "rule": label,
        "status": "pass" if passed else "fail",
        "message": f"✅ {label}" if passed else f"❌ {label} (your value: {actual})",
        "required_value": str(expected),
        "actual_value": str(actual),
    }


async def check_eligibility(scheme_id: str, user_profile: dict) -> dict:
    """
    Check if a user is eligible for a specific scheme.

    Returns:
        Detailed eligibility result with per-rule explanation.
    """
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        return {
            "error": f"Scheme '{scheme_id}' not found",
            "is_eligible": False,
        }

    rules = scheme["eligibility_rules"]["rules"]
    logic = scheme["eligibility_rules"].get("logic", "AND")

    rule_results = []
    for rule in rules:
        result = _evaluate_rule(rule, user_profile)
        rule_results.append(result)

    passed = [r for r in rule_results if r["status"] == "pass"]
    failed = [r for r in rule_results if r["status"] == "fail"]
    unknown = [r for r in rule_results if r["status"] == "unknown"]

    if logic == "AND":
        is_eligible = len(failed) == 0 and len(unknown) == 0
    else:  # OR
        is_eligible = len(passed) > 0

    # Build explanation
    explanation_parts = []
    if is_eligible:
        explanation_parts.append(f"You are eligible for {scheme['name']}!")
        for r in passed:
            explanation_parts.append(f"  {r['message']}")
    else:
        explanation_parts.append(f"You may not be eligible for {scheme['name']}.")
        for r in failed:
            explanation_parts.append(f"  {r['message']}")
        if unknown:
            explanation_parts.append("  Missing information:")
            for r in unknown:
                explanation_parts.append(f"    - {r['message']}")

    # Suggest alternatives if not eligible
    alternatives = []
    if not is_eligible:
        alternatives = _find_alternatives(user_profile, exclude_scheme=scheme_id)

    return {
        "scheme_id": scheme_id,
        "scheme_name": scheme["name"],
        "is_eligible": is_eligible,
        "rule_results": rule_results,
        "passed_count": len(passed),
        "failed_count": len(failed),
        "unknown_count": len(unknown),
        "explanation": "\n".join(explanation_parts),
        "required_documents": scheme["required_documents"],
        "alternatives": alternatives,
    }


def _find_alternatives(user_profile: dict, exclude_scheme: str = None, max_results: int = 3) -> list:
    """Find alternative schemes that the user might be eligible for."""
    all_schemes = get_all_schemes()
    candidates = []

    for scheme in all_schemes:
        if scheme["scheme_id"] == exclude_scheme:
            continue

        rules = scheme["eligibility_rules"]["rules"]
        passed = 0
        total = len(rules)

        for rule in rules:
            result = _evaluate_rule(rule, user_profile)
            if result["status"] == "pass":
                passed += 1

        if total > 0:
            match_ratio = passed / total
            if match_ratio > 0.3:  # At least 30% rules match
                candidates.append({
                    "scheme_id": scheme["scheme_id"],
                    "name": scheme["name"],
                    "category": scheme["category"],
                    "match_ratio": round(match_ratio, 2),
                    "benefits": scheme["benefits"],
                })

    candidates.sort(key=lambda x: x["match_ratio"], reverse=True)
    return candidates[:max_results]
