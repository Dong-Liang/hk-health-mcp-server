"""
Module for fetching waiting times for new case bookings for specialist outpatient services
by specialty and cluster in Hong Kong from Hospital Authority.
"""

from typing import Dict, List, Optional
import datetime
from pydantic import Field
from typing_extensions import Annotated
from hkopenai_common.json_utils import fetch_json_data





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
    url = f"https://www.ha.org.hk/opendata/sop/sop-waiting-time-{lang}.json"
    data = fetch_json_data(url)
    if "error" in data:
        return {"type": "Error", "error": data["error"]}
    return {"data": data, "last_updated": datetime.datetime.now().isoformat()}
