"""
Module for fetching waiting times for new case bookings for specialist outpatient services
by specialty and cluster in Hong Kong from Hospital Authority.
"""

import json
import urllib.request
import datetime
from typing import Dict, List, Optional

from pydantic import Field
from typing_extensions import Annotated


def fetch_specialist_waiting_data(lang: Optional[str] = "en") -> List[Dict]:
    """Fetch and parse specialist outpatient waiting time data from Hospital Authority

    Args:
        lang: Language code (en/tc/sc) for data format

    Returns:
        List of specialist waiting times with cluster, specialty, category, description, and value
    """
    url = f"https://www.ha.org.hk/opendata/sop/sop-waiting-time-{lang}.json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))

    return data


def register(mcp):
    """Registers the specialist waiting times tool with the FastMCP server."""

    @mcp.tool(
        description="Get current waiting times for new case bookings for specialist outpatient services by specialty and cluster in Hong Kong"
    )
    def get_specialist_waiting_times(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc) English, Traditional Chinese, Simplified Chinese. Default English",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
    ) -> Dict:
        return _get_specialist_waiting_times(lang)


def _get_specialist_waiting_times(lang: Optional[str] = "en") -> Dict:
    """Get current waiting times for new case bookings for specialist outpatient services

    Args:
        lang: Language code (en/tc/sc) for data format
    """
    data = fetch_specialist_waiting_data(lang)
    return {"data": data, "last_updated": datetime.datetime.now().isoformat()}
