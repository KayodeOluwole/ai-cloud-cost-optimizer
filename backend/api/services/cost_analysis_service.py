# backend/api/services/cost_analysis_service.py

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

from api.services.cost_service import fetch_all_costs


def _parse_date(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str)


def analyze_costs() -> Dict[str, Any]:
    """
    Analyze cost data and return:
    - structured insights (spikes, high-cost resources, unused resources, trends)
    - numeric scores
    - human-readable explanation
    """

    costs = fetch_all_costs()  # List[dict] from existing service

    if not costs:
        return {
            "summary": {
                "total_cost": 0,
                "currency": "USD",
                "num_records": 0,
                "num_resources": 0,
            },
            "spikes": [],
            "high_cost_resources": [],
            "unused_resources": [],
            "trends": {},
            "score": {
                "overall_health": 100,
                "cost_risk": 0,
                "waste_risk": 0,
            },
            "explanation": "No cost data available yet. The environment appears idle.",
        }

    # ---------- Aggregate basics ----------
    total_cost = 0.0
    currency = costs[0].get("currency", "USD")

    daily_totals = defaultdict(float)      # date -> total cost
    resource_totals = defaultdict(float)   # resource_id -> total cost
    resource_last_date = {}                # resource_id -> last usage date

    for row in costs:
        amount = float(row["cost_amount"])
        total_cost += amount

        date_str = row["usage_date"]
        resource_id = row["resource_id"]

        daily_totals[date_str] += amount
        resource_totals[resource_id] += amount

        date_obj = _parse_date(date_str)
        if resource_id not in resource_last_date or date_obj > resource_last_date[resource_id]:
            resource_last_date[resource_id] = date_obj

    num_records = len(costs)
    num_resources = len(resource_totals)

    # ---------- Detect daily spikes ----------
    spikes: List[Dict[str, Any]] = []
    dates_sorted = sorted(daily_totals.keys())
    for i in range(1, len(dates_sorted)):
        prev_date = dates_sorted[i - 1]
        cur_date = dates_sorted[i]
        prev_val = daily_totals[prev_date]
        cur_val = daily_totals[cur_date]

        if prev_val <= 0:
            continue

        change_pct = ((cur_val - prev_val) / prev_val) * 100.0
        severity = "info"
        if abs(change_pct) >= 70:
            severity = "critical"
        elif abs(change_pct) >= 40:
            severity = "high"
        elif abs(change_pct) >= 20:
            severity = "medium"

        if abs(change_pct) >= 20:  # threshold to record as spike
            spikes.append(
                {
                    "from_date": prev_date,
                    "to_date": cur_date,
                    "previous_total": round(prev_val, 2),
                    "current_total": round(cur_val, 2),
                    "change_percent": round(change_pct, 2),
                    "severity": severity,
                }
            )

    # ---------- High-cost resources ----------
    avg_per_resource = total_cost / max(num_resources, 1)
    high_cost_resources: List[Dict[str, Any]] = []
    for r_id, r_total in resource_totals.items():
        factor = r_total / avg_per_resource if avg_per_resource > 0 else 0
        if factor >= 1.5:  # 50% above average
            severity = "medium"
            if factor >= 2.0:
                severity = "high"
            high_cost_resources.append(
                {
                    "resource_id": r_id,
                    "total_cost": round(r_total, 2),
                    "relative_to_avg": round(factor, 2),
                    "severity": severity,
                }
            )

    # ---------- Unused / stale resources ----------
    # Define "stale" as not seen in the last 7 days relative to the latest date in data
    latest_date = max(resource_last_date.values())
    stale_threshold_days = 7
    unused_resources: List[Dict[str, Any]] = []

    for r_id, last_seen in resource_last_date.items():
        age_days = (latest_date - last_seen).days
        if age_days >= stale_threshold_days:
            unused_resources.append(
                {
                    "resource_id": r_id,
                    "last_usage_date": last_seen.date().isoformat(),
                    "days_since_last_use": age_days,
                    "estimated_savings_if_deleted": round(resource_totals[r_id], 2),
                }
            )

    # ---------- Trends ----------
    # Simple trend: compare first day vs last day
    first_date = dates_sorted[0]
    first_total = daily_totals[first_date]
    last_total = daily_totals[dates_sorted[-1]]

    trend_change_pct = None
    if first_total > 0:
        trend_change_pct = ((last_total - first_total) / first_total) * 100.0

    trends = {
        "first_day": {
            "date": first_date,
            "total_cost": round(first_total, 2),
        },
        "last_day": {
            "date": dates_sorted[-1],
            "total_cost": round(last_total, 2),
        },
        "overall_change_percent": round(trend_change_pct, 2) if trend_change_pct is not None else None,
    }

    # ---------- Scores ----------
    # Simple scoring rules you can tune later
    cost_risk = 0
    waste_risk = 0

    if spikes:
        max_spike = max(spikes, key=lambda s: abs(s["change_percent"]))
        if abs(max_spike["change_percent"]) >= 70:
            cost_risk += 50
        elif abs(max_spike["change_percent"]) >= 40:
            cost_risk += 30
        else:
            cost_risk += 15

    cost_risk += min(len(high_cost_resources) * 10, 30)
    waste_risk += min(len(unused_resources) * 10, 40)

    overall_health = max(0, 100 - (cost_risk + waste_risk))

    score = {
        "overall_health": overall_health,
        "cost_risk": cost_risk,
        "waste_risk": waste_risk,
    }

    # ---------- Human-readable explanation ----------
    explanation_parts = []

    explanation_parts.append(
        f"Total recorded spend is {round(total_cost, 2)} {currency} "
        f"across {num_resources} resources and {num_records} usage records."
    )

    if spikes:
        top_spike = max(spikes, key=lambda s: abs(s["change_percent"]))
        direction = "increase" if top_spike["change_percent"] > 0 else "decrease"
        explanation_parts.append(
            f"The largest day-over-day {direction} in cost was "
            f"{abs(top_spike['change_percent'])}% between "
            f"{top_spike['from_date']} and {top_spike['to_date']}."
        )
    else:
        explanation_parts.append("No significant day-over-day cost spikes were detected.")

    if high_cost_resources:
        top = sorted(high_cost_resources, key=lambda r: r["total_cost"], reverse=True)[0]
        explanation_parts.append(
            f"Resource '{top['resource_id']}' is a major cost driver at "
            f"{top['total_cost']} {currency}, which is "
            f"{top['relative_to_avg']}x the average resource cost."
        )
    else:
        explanation_parts.append("No resources are far above the average cost per resource.")

    if unused_resources:
        explanation_parts.append(
            f"{len(unused_resources)} resources look stale (no usage for at least "
            f"{stale_threshold_days} days) and may be candidates for cleanup."
        )
    else:
        explanation_parts.append("No obviously stale resources were detected in the recent data window.")

    explanation_parts.append(
        f"Overall cost health score is {overall_health}/100 "
        f"(cost risk: {cost_risk}, waste risk: {waste_risk})."
    )

    explanation = " ".join(explanation_parts)

    # ---------- Final payload ----------
    return {
        "summary": {
            "total_cost": round(total_cost, 2),
            "currency": currency,
            "num_records": num_records,
            "num_resources": num_resources,
        },
        "spikes": spikes,
        "high_cost_resources": high_cost_resources,
        "unused_resources": unused_resources,
        "trends": trends,
        "score": score,
        "explanation": explanation,
    }
