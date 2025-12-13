# backend/api/routers/cost_routes.py

from fastapi import APIRouter

# Existing service functions
from api.services.cost_service import (
    fetch_all_costs,
    fetch_latest_costs,
    fetch_cost_by_resource,
    fetch_cost_between_dates,
    cost_summary,
)

# NEW: Import the AI analysis module
from api.services.cost_analysis_service import analyze_costs

router = APIRouter(prefix="/costs", tags=["Cost Data"])


# ---------------------------------------------------------
# Existing Endpoints
# ---------------------------------------------------------

@router.get("/")
def get_all_costs():
    """Return all cost records."""
    return fetch_all_costs()


@router.get("/latest")
def get_latest_costs():
    """Return the most recent cost entries."""
    return fetch_latest_costs()


@router.get("/summary")
def get_cost_summary():
    """Return aggregated cost summary."""
    return cost_summary()


@router.get("/resource/{resource_id}")
def get_cost_for_resource(resource_id: str):
    """Return cost for a specific resource."""
    return fetch_cost_by_resource(resource_id)


@router.get("/dates")
def get_cost_between(start: str, end: str):
    """
    Return cost data between two dates.
    Example: /costs/dates?start=2025-02-01&end=2025-02-10
    """
    return fetch_cost_between_dates(start, end)


# ---------------------------------------------------------
# NEW – AI ANALYSIS ENDPOINT
# ---------------------------------------------------------

@router.get("/analysis")
def get_cost_analysis():
    """
    Run AI-style cost analysis:
    - detect cost spikes
    - detect unused resources
    - identify high-cost resources
    - trends
    - risk scoring
    - human-readable explanation
    """
    return analyze_costs()
@router.get("/costs/summary")
def get_cost_summary():
    # Group cost by category
    category_totals = {}
    for item in COST_DATA:
        cat = item["meterCategory"]
        category_totals[cat] = category_totals.get(cat, 0) + item["cost_amount"]

    # Daily trend
    daily_trend = {}
    for item in COST_DATA:
        day = item["usage_date"]
        daily_trend[day] = daily_trend.get(day, 0) + item["cost_amount"]

    return {
        "category_totals": category_totals,
        "daily_trend": daily_trend
    }

