"""
Module for fetching Accident and Emergency Department (AED) waiting times
from Hospital Authority in Hong Kong.
"""

import json
import urllib.request
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import Field
from typing_extensions import Annotated


def fetch_aed_waiting_data(lang: Optional[str] = "en") -> Dict:
    """Fetch and parse AED waiting time data from Hospital Authority

    Args:
        lang: Language code (en/tc/sc) for data format

    Returns:
        List of hospital waiting times with hospital_name, waiting_time, update_time
    """
    url = f"https://www.ha.org.hk/opendata/aed/aedwtdata-{lang}.json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))

    # Transform new data format to expected format
    return data


def register(mcp):
    """Registers the AED waiting times tool with the FastMCP server."""

    @mcp.tool(
        description="Get current Accident and Emergency Department waiting times by hospital in Hong Kong"
    )
    def get_aed_waiting_times(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc) English, Traditional Chinese, Simplified Chinese. Default English",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
    ) -> Dict:
        """Get current AED waiting times

        Args:
            lang: Language code (en/tc/sc) for data format
        """
        return _get_aed_waiting_times(lang)


def _get_aed_waiting_times(lang: Optional[str] = "en") -> Dict:
    """Get current AED waiting times

    Args:
        lang: Language code (en/tc/sc) for data format
    """
    data = fetch_aed_waiting_data(lang)
    return {"data": data, "last_updated": datetime.now().isoformat()}
