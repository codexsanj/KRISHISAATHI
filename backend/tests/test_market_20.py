"""
Market Intelligence Test Suite 2.0

Tests the production pipeline: data.gov.in → market_data_provider → MarketService → API
All external API calls are mocked. No real network requests.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import requests

from app.main import app
from app.services.market_service import market_service, MarketService, SUPPORTED_COMMODITIES_LIST

client = TestClient(app)


# ── Fixtures: realistic data.gov.in API responses ────────────────────────────

MOCK_GINGER_RECORDS = [
    {
        "state": "Karnataka",
        "district": "Hassan",
        "market": "Hassan APMC",
        "commodity": "Ginger",
        "variety": "Fresh Ginger",
        "arrival_date": "2026-08-20",
        "min_price": "4200",
        "max_price": "5400",
        "modal_price": "4900",
    },
    {
        "state": "Karnataka",
        "district": "Bengaluru",
        "market": "Yeshwanthpur APMC",
        "commodity": "Ginger",
        "variety": "Dry Ginger",
        "arrival_date": "2026-08-20",
        "min_price": "4600",
        "max_price": "5800",
        "modal_price": "5200",
    },
    {
        "state": "Kerala",
        "district": "Wayanad",
        "market": "Wayanad Mandi",
        "commodity": "Ginger",
        "variety": "Fresh Ginger",
        "arrival_date": "2026-08-19",
        "min_price": "4800",
        "max_price": "6100",
        "modal_price": "5400",
    },
]

MOCK_HISTORICAL_RECORDS = [
    {
        "state": "Karnataka",
        "district": "Hassan",
        "market": "Hassan APMC",
        "commodity": "Ginger",
        "variety": "Fresh Ginger",
        "arrival_date": "2026-08-18",
        "min_price": "4100",
        "max_price": "5200",
        "modal_price": "4700",
    },
    {
        "state": "Karnataka",
        "district": "Hassan",
        "market": "Hassan APMC",
        "commodity": "Ginger",
        "variety": "Fresh Ginger",
        "arrival_date": "2026-08-19",
        "min_price": "4200",
        "max_price": "5300",
        "modal_price": "4800",
    },
    {
        "state": "Karnataka",
        "district": "Hassan",
        "market": "Hassan APMC",
        "commodity": "Ginger",
        "variety": "Fresh Ginger",
        "arrival_date": "2026-08-20",
        "min_price": "4300",
        "max_price": "5400",
        "modal_price": "4900",
    },
]


def _mock_current_prices(records):
    """Helper: patches fetch_current_prices to return given records."""
    return patch(
        "app.services.market_data_provider.market_data_provider.fetch_current_prices",
        return_value=records,
    )


def _mock_historical_prices(records):
    """Helper: patches fetch_historical_prices to return given records."""
    return patch(
        "app.services.market_data_provider.market_data_provider.fetch_historical_prices",
        return_value=records,
    )


def _mock_both(current_records, historical_records):
    """Helper: patches both provider methods."""
    p1 = patch(
        "app.services.market_data_provider.market_data_provider.fetch_current_prices",
        return_value=current_records,
    )
    p2 = patch(
        "app.services.market_data_provider.market_data_provider.fetch_historical_prices",
        return_value=historical_records,
    )
    return p1, p2


# ── 1. Supported Commodities & Search ────────────────────────────────────────

class TestCommodityCatalog:

    def test_40_plus_supported_crops(self):
        crops = market_service.get_supported_crops()
        assert len(crops) >= 40
        for expected in ["Rice", "Wheat", "Ginger", "Tomato", "Onion", "Potato"]:
            assert expected in crops

    def test_search_finds_partial_match(self):
        assert "Ginger" in market_service.search_commodities("gin")
        assert "Tomato" in market_service.search_commodities("tom")

    def test_search_empty_returns_all(self):
        result = market_service.search_commodities("")
        assert result == SUPPORTED_COMMODITIES_LIST

    def test_resolve_crop_alias(self):
        ms = MarketService()
        assert ms.resolve_crop_name("paddy") == "Rice"
        assert ms.resolve_crop_name("corn") == "Maize"
        assert ms.resolve_crop_name("fresh ginger") == "Ginger"

    def test_resolve_crop_empty_defaults_to_ginger(self):
        ms = MarketService()
        assert ms.resolve_crop_name("") == "Ginger"


# ── 2. Normalized Schema Verification ────────────────────────────────────────

CANONICAL_FIELDS = [
    "commodity", "market", "state", "district", "date",
    "min_price", "max_price", "modal_price", "average_price",
    "unit", "source",
]


class TestNormalizedSchema:

    def test_canonical_fields_present(self):
        """Every normalized record must have exactly the canonical fields."""
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            prices = market_service.get_prices("Ginger")
        assert len(prices) == 3
        for record in prices:
            for field in CANONICAL_FIELDS:
                assert field in record, f"Missing field: {field}"

    def test_price_values_are_float(self):
        """Prices coming as strings from data.gov.in must be converted to float."""
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            prices = market_service.get_prices("Ginger")
        top = prices[0]
        assert isinstance(top["modal_price"], float)
        assert isinstance(top["min_price"], float)
        assert isinstance(top["max_price"], float)
        assert isinstance(top["average_price"], float)

    def test_price_values_are_correct(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            prices = market_service.get_prices("Ginger")
        top = prices[0]
        assert top["modal_price"] == 4900.0
        assert top["min_price"] == 4200.0
        assert top["max_price"] == 5400.0
        assert top["unit"] == "₹/quintal"
        assert top["source"] == "AGMARKNET"

    def test_state_district_market_mapped(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            prices = market_service.get_prices("Ginger")
        top = prices[0]
        assert top["state"] == "Karnataka"
        assert top["district"] == "Hassan"
        assert top["market"] == "Hassan APMC"
        assert top["commodity"] == "Ginger"
        assert top["date"] == "2026-08-20"


# ── 3. Missing Prices ────────────────────────────────────────────────────────

class TestMissingPrices:

    def test_missing_modal_price_yields_none(self):
        """If modal_price is absent, it must be None — not 0 or undefined."""
        record = [{"state": "Karnataka", "district": "Hassan", "market": "Hassan APMC"}]
        with _mock_current_prices(record):
            prices = market_service.get_prices("Ginger")
        assert prices[0]["modal_price"] is None
        assert prices[0]["min_price"] is None
        assert prices[0]["max_price"] is None
        assert prices[0]["average_price"] is None

    def test_missing_min_max_derives_from_modal(self):
        """If only modal_price exists, min/max should be derived (0.85x / 1.15x)."""
        record = [{"state": "Karnataka", "district": "Hassan", "market": "Hassan APMC",
                    "modal_price": "5000"}]
        with _mock_current_prices(record):
            prices = market_service.get_prices("Ginger")
        p = prices[0]
        assert p["modal_price"] == 5000.0
        assert p["min_price"] == round(5000 * 0.85, 2)
        assert p["max_price"] == round(5000 * 1.15, 2)

    def test_missing_min_only(self):
        """If min_price is missing but max and modal exist, min derives from modal."""
        record = [{"state": "Karnataka", "district": "Hassan", "market": "Hassan APMC",
                    "modal_price": "5000", "max_price": "5500"}]
        with _mock_current_prices(record):
            prices = market_service.get_prices("Ginger")
        p = prices[0]
        assert p["modal_price"] == 5000.0
        assert p["max_price"] == 5500.0
        assert p["min_price"] == round(5000 * 0.85, 2)


# ── 4. Invalid Prices ────────────────────────────────────────────────────────

class TestInvalidPrices:

    @pytest.mark.parametrize("bad_value", [
        "not_a_number",
        "",
        "N/A",
        "₹5000",
        "five thousand",
    ])
    def test_invalid_string_prices_become_none(self, bad_value):
        record = [{"state": "Karnataka", "district": "Hassan", "market": "Hassan APMC",
                    "modal_price": bad_value, "min_price": bad_value, "max_price": bad_value}]
        with _mock_current_prices(record):
            prices = market_service.get_prices("Ginger")
        p = prices[0]
        assert p["modal_price"] is None
        assert p["min_price"] is None
        assert p["max_price"] is None

    def test_none_prices_become_none(self):
        record = [{"state": "Karnataka", "district": "Hassan", "market": "Hassan APMC",
                    "modal_price": None, "min_price": None, "max_price": None}]
        with _mock_current_prices(record):
            prices = market_service.get_prices("Ginger")
        p = prices[0]
        assert p["modal_price"] is None
        assert p["min_price"] is None
        assert p["max_price"] is None


# ── 5. Empty Provider Response ────────────────────────────────────────────────

class TestEmptyProviderResponse:

    def test_get_prices_returns_empty_list(self):
        with _mock_current_prices([]):
            prices = market_service.get_prices("Ginger")
        assert prices == []

    def test_get_popular_crops_summary_returns_empty_no_exception(self):
        """The fixed bug: must NOT raise IndexError on empty provider response."""
        with _mock_current_prices([]):
            result = market_service.get_popular_crops_summary()
        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_popular_crops_summary_with_farmer_crop_empty(self):
        with _mock_current_prices([]):
            result = market_service.get_popular_crops_summary(farmer_crop="Rice")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_historical_prices_empty(self):
        with _mock_historical_prices([]):
            hist = market_service.get_historical_prices("Ginger", days=30)
        assert hist["commodity"] == "Ginger"
        assert hist["history"] == []
        assert hist["current_modal_price"] is None
        assert hist["trend"] == "FLAT"

    def test_get_market_trend_empty(self):
        with _mock_current_prices([]):
            trend = market_service.get_market_trend("Ginger")
        assert trend["highest_market"] == "Unavailable"
        assert trend["highest_price"] == 0


# ── 6. Provider Network Failures ─────────────────────────────────────────────

class TestProviderFailures:

    def test_timeout_returns_empty(self):
        with patch("app.services.market_data_provider.requests.get",
                    side_effect=requests.exceptions.Timeout("Connection timed out")):
            from app.services.market_data_provider import DataGovInProvider
            provider = DataGovInProvider(api_key="test_key")
            result = provider.fetch_current_prices("Ginger")
        assert result == []

    def test_connection_error_returns_empty(self):
        with patch("app.services.market_data_provider.requests.get",
                    side_effect=requests.exceptions.ConnectionError("Network unreachable")):
            from app.services.market_data_provider import DataGovInProvider
            provider = DataGovInProvider(api_key="test_key")
            result = provider.fetch_current_prices("Ginger")
        assert result == []

    def test_http_500_returns_empty(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        with patch("app.services.market_data_provider.requests.get", return_value=mock_resp):
            from app.services.market_data_provider import DataGovInProvider
            provider = DataGovInProvider(api_key="test_key")
            result = provider.fetch_current_prices("Ginger")
        assert result == []

    def test_http_403_returns_empty(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        with patch("app.services.market_data_provider.requests.get", return_value=mock_resp):
            from app.services.market_data_provider import DataGovInProvider
            provider = DataGovInProvider(api_key="test_key")
            result = provider.fetch_current_prices("Ginger")
        assert result == []

    def test_missing_api_key_returns_empty(self):
        from app.services.market_data_provider import DataGovInProvider
        provider = DataGovInProvider(api_key="")
        result = provider.fetch_current_prices("Ginger")
        assert result == []


# ── 7. Filter Pass-through ────────────────────────────────────────────────────

class TestFilters:

    def test_state_filter_passed_to_provider(self):
        """Verifies filters are passed through and commodity name is mapped to data.gov.in format."""
        with patch(
            "app.services.market_data_provider.market_data_provider.fetch_current_prices",
            return_value=[],
        ) as mock_fetch:
            market_service.get_prices("Ginger", state="Karnataka")
            mock_fetch.assert_called_once_with(
                commodity="Ginger(Green)", state="Karnataka", district=None, market=None
            )

    def test_all_filters_passed_to_provider(self):
        """Verifies all filters are passed through and commodity name is mapped."""
        with patch(
            "app.services.market_data_provider.market_data_provider.fetch_current_prices",
            return_value=[],
        ) as mock_fetch:
            market_service.get_prices(
                "Ginger", state="Karnataka", district="Hassan", market="Hassan APMC"
            )
            mock_fetch.assert_called_once_with(
                commodity="Ginger(Green)", state="Karnataka",
                district="Hassan", market="Hassan APMC",
            )

    def test_states_list(self):
        states = market_service.get_states()
        assert "Karnataka" in states
        assert "Maharashtra" in states
        assert states == sorted(states)  # alphabetical

    def test_districts_for_state(self):
        districts = market_service.get_districts("Karnataka")
        assert "Hassan" in districts
        assert "Bengaluru" in districts

    def test_markets_for_district(self):
        markets = market_service.get_markets("Karnataka", "Hassan")
        assert "Hassan APMC" in markets


# ── 8. Historical Data ───────────────────────────────────────────────────────

class TestHistoricalData:

    def test_valid_historical_response(self):
        with _mock_historical_prices(MOCK_HISTORICAL_RECORDS):
            hist = market_service.get_historical_prices("Ginger", days=30)
        assert hist["commodity"] == "Ginger"
        assert len(hist["history"]) == 3
        assert hist["current_modal_price"] is not None
        assert hist["lowest_price"] is not None
        assert hist["highest_price"] is not None
        assert hist["average_price"] is not None
        assert hist["source"] == "AGMARKNET"
        assert hist["trend"] in ("UPWARD", "DOWNWARD")

    def test_historical_records_have_canonical_fields(self):
        with _mock_historical_prices(MOCK_HISTORICAL_RECORDS):
            hist = market_service.get_historical_prices("Ginger", days=30)
        for record in hist["history"]:
            for field in CANONICAL_FIELDS:
                assert field in record, f"Missing field in history record: {field}"

    def test_historical_sorted_by_date(self):
        with _mock_historical_prices(MOCK_HISTORICAL_RECORDS):
            hist = market_service.get_historical_prices("Ginger", days=30)
        dates = [r["date"] for r in hist["history"]]
        assert dates == sorted(dates)


# ── 9. Market Comparison ─────────────────────────────────────────────────────

class TestMarketComparison:

    def test_compare_with_multiple_records(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            r = client.get("/api/market/compare?crop=Ginger")
        assert r.status_code == 200
        data = r.json()
        assert data["crop"] == "Ginger"
        assert len(data["comparison"]) == 3
        assert data["highest_price"] >= data["lowest_price"]
        assert data["average_price"] > 0

    def test_compare_empty_returns_no_data(self):
        with _mock_current_prices([]):
            r = client.get("/api/market/compare?crop=Ginger")
        assert r.status_code == 200
        data = r.json()
        assert data["comparison"] == []


# ── 10. Popular Crops Summary (with data) ────────────────────────────────────

class TestPopularCropsSummary:

    def test_popular_with_data_returns_cards(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            result = market_service.get_popular_crops_summary()
        assert len(result) > 0
        card = result[0]
        assert "commodity" in card
        assert "modal_price" in card
        assert "unit" in card
        assert card["unit"] == "₹/quintal"
        assert card["source"] == "AGMARKNET"
        assert card["markets_count"] == 3

    def test_popular_card_has_valid_price(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            result = market_service.get_popular_crops_summary()
        card = result[0]
        assert isinstance(card["modal_price"], float)
        assert card["modal_price"] > 0


# ── 11. API Endpoint Integration (mocked provider) ──────────────────────────

class TestAPIEndpoints:

    def test_crops_endpoint(self):
        r = client.get("/api/market/crops")
        assert r.status_code == 200
        assert r.json()["count"] >= 40

    def test_search_endpoint(self):
        r = client.get("/api/market/crops/search?q=rice")
        assert r.status_code == 200
        assert "Rice" in r.json()["matches"]

    def test_states_endpoint(self):
        r = client.get("/api/market/states")
        assert r.status_code == 200
        assert "Karnataka" in r.json()

    def test_districts_endpoint(self):
        r = client.get("/api/market/districts?state=Karnataka")
        assert r.status_code == 200
        assert "Hassan" in r.json()

    def test_prices_endpoint_with_data(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            r = client.get("/api/market/prices/current?crop=Ginger")
        assert r.status_code == 200
        data = r.json()
        assert data["commodity"] == "Ginger"
        assert len(data["prices"]) == 3

    def test_prices_endpoint_empty(self):
        with _mock_current_prices([]):
            r = client.get("/api/market/prices/current?crop=Ginger")
        assert r.status_code == 200
        assert r.json()["prices"] == []

    def test_popular_endpoint_empty(self):
        with _mock_current_prices([]):
            r = client.get("/api/market/popular")
        assert r.status_code == 200
        assert r.json() == []

    def test_history_endpoint_with_data(self):
        with _mock_historical_prices(MOCK_HISTORICAL_RECORDS):
            r = client.get("/api/market/prices/history?crop=Ginger&days=30")
        assert r.status_code == 200
        data = r.json()
        assert data["commodity"] == "Ginger"
        assert len(data["history"]) == 3

    def test_history_endpoint_empty(self):
        with _mock_historical_prices([]):
            r = client.get("/api/market/prices/history?crop=Ginger&days=30")
        assert r.status_code == 200
        data = r.json()
        assert data["history"] == []

    def test_trends_endpoint_with_data(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            r = client.get("/api/market/trends?crop=Ginger")
        assert r.status_code == 200
        data = r.json()
        assert data["highest_price"] > 0

    def test_trends_endpoint_empty(self):
        with _mock_current_prices([]):
            r = client.get("/api/market/trends?crop=Ginger")
        assert r.status_code == 200
        data = r.json()
        assert data["highest_market"] == "Unavailable"


# ── 12. ₹undefined Regression ────────────────────────────────────────────────

class TestRupeeUndefinedRegression:
    """
    Regression: the frontend formatPrice() uses typeof p === 'number'.
    If any price field is a non-numeric type (string, undefined, NaN),
    the UI would render ₹undefined / ₹null / ₹NaN.
    These tests verify the backend NEVER sends such values.
    """

    def test_valid_prices_are_always_float(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            prices = market_service.get_prices("Ginger")
        for p in prices:
            for field in ["modal_price", "min_price", "max_price", "average_price"]:
                val = p[field]
                assert val is None or isinstance(val, float), (
                    f"{field}={val!r} (type={type(val).__name__}) — "
                    f"must be float or None, never str/int/NaN"
                )

    def test_missing_prices_are_none_not_string(self):
        record = [{"state": "Karnataka", "district": "Hassan", "market": "Hassan APMC"}]
        with _mock_current_prices(record):
            prices = market_service.get_prices("Ginger")
        p = prices[0]
        for field in ["modal_price", "min_price", "max_price", "average_price"]:
            assert p[field] is None, (
                f"{field} should be None when data is missing, got {p[field]!r}"
            )

    def test_invalid_prices_are_none_not_nan(self):
        record = [{"state": "Karnataka", "district": "Hassan", "market": "Hassan APMC",
                    "modal_price": "abc", "min_price": "xyz", "max_price": ""}]
        with _mock_current_prices(record):
            prices = market_service.get_prices("Ginger")
        p = prices[0]
        import math
        for field in ["modal_price", "min_price", "max_price", "average_price"]:
            val = p[field]
            assert val is None or not math.isnan(val), (
                f"{field} must not be NaN, got {val!r}"
            )

    def test_popular_summary_prices_never_string(self):
        with _mock_current_prices(MOCK_GINGER_RECORDS):
            cards = market_service.get_popular_crops_summary()
        for card in cards:
            for field in ["modal_price", "average_price", "min_price", "max_price"]:
                val = card.get(field)
                assert val is None or isinstance(val, float), (
                    f"Popular card {card['commodity']}: {field}={val!r} must be float or None"
                )
