"""Stream type classes for Criteo version 2023-01."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


from dateutil.parser import parse
from singer_sdk.plugin_base import PluginBase as TapBaseClass
import singer_sdk._singerlib as singer

from tap_criteo.client import CriteoSearchStream, CriteoStream
from tap_criteo.streams.reports import dimensions, metrics, analytics_type_mappings, value_func_mapping

SCHEMAS_DIR = Path(__file__).parent.parent / "./schemas"
API_VERSION = "2023-01"

class CampaignsStream(CriteoSearchStream):
    """Campaigns stream."""

    name = "campaigns"
    path = f"/{API_VERSION}/marketing-solutions/campaigns/search"
    schema_filepath = SCHEMAS_DIR / "campaign.json"
    
class AudiencesStream(CriteoStream):
    """Audiences stream."""

    name = "audiences"
    path = f"/{API_VERSION}/audiences"
    schema_filepath = SCHEMAS_DIR / "audience.json"


class AdvertisersStream(CriteoStream):
    """Advertisers stream."""

    name = "advertisers"
    path = f"/{API_VERSION}/advertisers/me"
    schema_filepath = SCHEMAS_DIR / "advertiser.json"


class AdSetsStream(CriteoSearchStream):
    """Ad sets stream."""

    name = "ad_sets"
    path = f"/{API_VERSION}/marketing-solutions/ad-sets/search"
    schema_filepath = SCHEMAS_DIR / "ad_set.json"


class StatsReportStream(CriteoStream):
    """Statistics reports stream."""

    name = "statistics"
    path = f"/{API_VERSION}/statistics/report"
    records_jsonpath = "$.Rows[*]"
    rest_method = "POST"
    replication_key = "Day"

    @property
    def primary_keys(self):
        """Return primary key dynamically based on user inputs."""
        return self.dimensions
    
    @primary_keys.setter
    def primary_keys(self, value):
        pass

    def __init__(
        self,
        tap: TapBaseClass
    ) -> None:
        """Initialize a stats report stream.

        Args:
            tap: The tap instance.
            report: The report dictionary.
        """
        self.dimensions = []
        self.metrics = []

        schema = {"properties": analytics_type_mappings}

        super().__init__(tap, schema=schema)

    # def _write_schema_message(self) -> None:
    #     CriteoStream._write_schema_message(self)

    def apply_catalog(self, catalog: singer.Catalog) -> None:
        """Extract the dimensions and metrics from the catalog."""

        catalog_entry = catalog.get_stream(self.name)
        selection = catalog_entry.metadata.resolve_selection()

        for breadcrumb, selected in selection.items():
            if breadcrumb and selected:
                if breadcrumb[-1] in dimensions:
                    self.dimensions.append(breadcrumb[-1])
                elif breadcrumb[-1] in metrics and breadcrumb[-1] != "Currency":
                    self.metrics.append(breadcrumb[-1])

        catalog_entry.key_properties = self.dimensions
        catalog_entry.metadata.root.table_key_properties = catalog_entry.key_properties
        # Hack to remove stream mapping as it interferes 
        # with the above key_properties overrides. The better way would be to 
        # edit the stream mapper itself to allow for key_properties overrides.
        self._tap.mapper = None
        
        self.logger.info("Computed DIMENSIONS: %s", self.dimensions)
        self.logger.info("Computed METRICS: %s", self.metrics)
        self.logger.info("Computed PRIMARY KEYS: %s", self.primary_keys)

        super().apply_catalog(catalog)

    def prepare_request_payload(
        self,
        context: dict | None,
        next_page_token: Any,
    ) -> dict:
        """Prepare request payload.

        Args:
            context: Stream context.
            next_page_token: The next page value.
        Returns:
            Dictionary for the JSON body of the request.
        """
        start_date = parse(self.config["start_date"])
        end_date = self.config.get("end_date")
        
        if end_date:
            end_date = parse(end_date)
        else:
            end_date = datetime.utcnow()

        return {
            "dimensions": self.dimensions,
            "metrics": self.metrics,
            "currency": self.config['currency'],
            "format": "json",
            "timezone": "UTC",
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
        }

    def post_process(self, row: dict, context: dict | None) -> dict:
        """Process the record before emitting it.

        Args:
            row: Record dictionary.
            context: Stream context.

        Returns:
            Mutated record dictionary.
        """

        for key in row:
            self.logger.info("Key: %s", key)
            func = value_func_mapping.get(key)
            if func:
                row[key] = func(row[key])

        row["Currency"] = self.config['currency']

        return row

