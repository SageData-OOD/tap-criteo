"""Criteo tap class."""

from typing import Dict, List, Type

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_criteo.client import CriteoStream
from tap_criteo.streams import v202301


OBJECT_STREAMS: Dict[str, List[Type[CriteoStream]]] = {
    "current": [
        v202301.AudiencesStream,
        v202301.AdvertisersStream,
        v202301.AdSetsStream,
        v202301.CampaignsStream,

    ]
}

REPORTS_BASE = v202301.StatsReportStream


class TapCriteo(Tap):
    """Criteo tap class."""

    name = "tap-criteo"

    config_jsonschema = th.PropertiesList(
        th.Property("client_id", th.StringType, required=True),
        th.Property("client_secret", th.StringType, required=True),
        th.Property("currency", th.StringType, default="USD"),
        th.Property("start_date", th.DateTimeType, required=True),
        th.Property("end_date", th.DateTimeType, required=False),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams.

        Returns:
            List of stream instances.
        """
        objects = [
            stream_class(tap=self)
            for api in ("current",)
            for stream_class in OBJECT_STREAMS[api]
        ]

        reports = [
            REPORTS_BASE(tap=self)
        ]

        return objects + reports
