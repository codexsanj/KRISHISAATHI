from fastapi import APIRouter, Query, Depends
from typing import Optional, List, Dict, Any
from app.services.market_service import market_service
from app.ai.farm_intelligence.selling_decision_engine import selling_decision_engine

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/crops")
def get_supported_crops():
    return {
        "count": len(market_service.get_supported_crops()),
        "crops": market_service.get_supported_crops()
    }


@router.get("/crops/search")
def search_crops(q: str = Query("")):
    matches = market_service.search_commodities(q)
    return {
        "query": q,
        "matches": matches
    }


@router.get("/states")
def get_states():
    return market_service.get_states()


@router.get("/districts")
def get_districts(state: str = Query("Karnataka")):
    return market_service.get_districts(state)


@router.get("/markets")
def get_markets(state: str = Query("Karnataka"), district: str = Query("Hassan")):
    return market_service.get_markets(state, district)


@router.get("/popular")
def get_popular_crops(farmer_crop: Optional[str] = Query(None)):
    return market_service.get_popular_crops_summary(farmer_crop)


@router.get("/prices")
@router.get("/prices/current")
@router.get("/current")
def get_current_market_prices(
    crop: Optional[str] = Query("Ginger"),
    state: Optional[str] = Query(None),
    district: Optional[str] = Query(None),
    market: Optional[str] = Query(None)
):
    prices = market_service.get_prices(commodity=crop, state=state, district=district, market=market)
    return {
        "commodity": crop,
        "prices": prices
    }


@router.get("/prices/history")
def get_price_history(crop: Optional[str] = Query("Ginger"), days: int = Query(30)):
    return market_service.get_historical_prices(commodity=crop, days=days)


@router.get("/trends")
def get_market_trends(crop: Optional[str] = Query("Ginger")):
    return market_service.get_market_trend(crop)


@router.get("/compare")
def compare_markets(crop: Optional[str] = Query("Ginger")):
    prices = market_service.get_prices(crop)
    if not prices:
        return {"crop": crop, "comparison": []}
    valid_prices = [p for p in prices if p.get("modal_price") is not None]
    if not valid_prices:
        return {"crop": crop, "comparison": []}

    highest = max(valid_prices, key=lambda x: x["modal_price"])
    lowest = min(valid_prices, key=lambda x: x["modal_price"])
    avg_price = sum(p["modal_price"] for p in valid_prices) / len(valid_prices)

    return {
        "crop": crop,
        "highest_market": highest.get("market"),
        "highest_price": highest["modal_price"],
        "lowest_market": lowest.get("market"),
        "lowest_price": lowest["modal_price"],
        "average_price": round(avg_price, 2),
        "comparison": prices
    }


@router.get("/selling")
@router.get("/selling-strategy")
def get_selling_strategy(
    crop: Optional[str] = Query("Ginger"),
    quantity_q: float = Query(10.0),
    location: Optional[str] = Query(None)
):
    return selling_decision_engine.evaluate_selling_strategy(crop, quantity_q, location)
