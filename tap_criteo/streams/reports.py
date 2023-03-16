"""Report fields."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Dict

dimensions = {
    # "Ad": {"type": "string"},
    # "AdId": {"type": "string"},
    "Adset": {"type": "string"},
    "AdsetId": {"type": "string"},
    "Campaign": {"type": "string"},
    "CampaignId": {"type": "string"},
    "Advertiser": {"type": "string"},
    "AdvertiserId": {"type": "string"},
    # "Category": {"type": "string"},
    # "CategoryId": {"type": "string"},
    "OS": {"type": "string"},
    "Device": {"type": "string"},
    "MarketingObjective": {"type": "string"},
    "MarketingObjectiveId": {"type": "string"},
    "CouponId": {"type": "string"}, 
    "Coupon": {"type": "string"},
    # "Year": {"type": "string", "format": "date"},
    # "Month": {"type": "string", "format": "date"},
    # "Week": {"type": "string", "format": "date"},
    "Day": {"type": "string", "format": "date"},
    # "Hour": {"type": "string", "format": "date-time"},
}

#list of criteo metrics for campaigns from https://developers.criteo.com/marketing-solutions/docs/campaign-statistics#metrics
metrics = {
    "Currency": {"type": "string"},
    "Clicks": {"type": "integer"},
    "Displays": {"type": "integer"},
    "Visits": {"type": "integer"},
    "AdvertiserCost": {"type": "number"},
    "SalesClientAttribution": {"type": "integer"},
    "SalesAllClientAttribution": {"type": "integer"},
    "SalesPc30d": {"type": "integer"},
    "SalesAllPc30d": {"type": "integer"},
    "SalesPv24h": {"type": "integer"},
    "SalesAllPv24h": {"type": "integer"},
    "SalesPc30dPv24h": {"type": "integer"},
    "SalesAllPc30dPv24h": {"type": "integer"},
    "SalesPc1d": {"type": "integer"},
    "SalesAllPc1d": {"type": "integer"},
    "SalesPc7d": {"type": "integer"},
    "SalesAllPc7d": {"type": "integer"},
    "RevenueGeneratedClientAttribution": {"type": "number"},
    "RevenueGeneratedAllClientAttribution": {"type": "number"},
    "RevenueGeneratedPc30d": {"type": "number"},
    "RevenueGeneratedAllPc30d": {"type": "number"},
    "RevenueGeneratedPv24h": {"type": "number"},
    "RevenueGeneratedAllPv24h": {"type": "number"},
    "RevenueGeneratedPc30dPv24h": {"type": "number"},
    "RevenueGeneratedAllPc30dPv24h": {"type": "number"},
    "RevenueGeneratedPc1d": {"type": "number"},
    "RevenueGeneratedAllPc1d": {"type": "number"},
    "RevenueGeneratedPc7d": {"type": "number"},
    "RevenueGeneratedAllPc7d": {"type": "number"}
}

# merge dimensions and metrics
analytics_type_mappings = {**dimensions, **metrics}

# TODO: reduce repetition here?
value_func_mapping: Dict[str, Callable[[str], Any]] = {
    "Date": lambda hour: datetime.strptime(hour, "%m/%d/%Y %H:%M:%S"),
    "Clicks": int,
    "Displays": int,
    "Visits": int,
    "AdvertiserCost": Decimal,
    # Sales
    "SalesClientAttribution": int,
    "SalesAllClientAttribution": int,
    "SalesPc30d": int,
    "SalesAllPc30d": int,
    "SalesPv24h": int,
    "SalesAllPv24h": int,
    "SalesPc30dPv24h": int,
    "SalesAllPc30dPv24h": int,
    "SalesPc1d": int,
    "SalesAllPc1d": int,
    "SalesPc7d": int,
    "SalesAllPc7d": int,
    # Revenue
    "RevenueGeneratedClientAttribution": Decimal,
    "RevenueGeneratedAllClientAttribution": Decimal,
    "RevenueGeneratedPc30d": Decimal,
    "RevenueGeneratedAllPc30d": Decimal,
    "RevenueGeneratedPv24h": Decimal,
    "RevenueGeneratedAllPv24h": Decimal,
    "RevenueGeneratedPc30dPv24h": Decimal,
    "RevenueGeneratedAllPc30dPv24h": Decimal,
    "RevenueGeneratedPc1d": Decimal,
    "RevenueGeneratedAllPc1d": Decimal,
    "RevenueGeneratedPc7d": Decimal,
    "RevenueGeneratedAllPc7d": Decimal,
}
