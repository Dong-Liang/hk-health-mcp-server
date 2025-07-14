"""
Module for fetching average number of general outpatient clinic quotas
for the preceding 4 weeks across districts in Hong Kong from Hospital Authority.
"""

from datetime import datetime
from typing import Dict, List, Optional
import requests

from pydantic import Field
from typing_extensions import Annotated


def fetch_pas_gopc_avg_quota_data(lang: str = "en") -> List[Dict]:
    """Fetch and parse average number of general outpatient clinic quota data for the preceding 4 weeks from Hospital Authority

    Args:
        lang: Language code (en/tc/sc) for data format

    Returns:
        List of clinic quota data with period, district, clinic name, consultation sessions, and daily averages
    """
    url = (
        f"https://www.ha.org.hk/pas_gopc/pas_gopc_avg_quota_pdf/g0_9uo7a_p-{lang}.json"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return data





def register(mcp):
    """Registers the general outpatient clinic quotas tool with the FastMCP server."""

    @mcp.tool(
        description="Get average number of general outpatient clinic quotas for the preceding 4 weeks across 18 districts in Hong Kong"
    )
    def get_pas_gopc_avg_quota(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc) English, Traditional Chinese, Simplified Chinese. Default English",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
        district: Annotated[
            Optional[str],
            Field(
                description="Optional: Filter by district name (e.g., 'Tuen Mun'). If not provided, data for all districts will be returned."
            ),
        ] = "",
    ) -> Dict:
        return _get_pas_gopc_avg_quota(lang, district)


def _get_pas_gopc_avg_quota(lang: str = "en", district: str = "") -> Dict:
    """Get average number of general outpatient clinic quotas for the preceding 4 weeks

    Args:
        lang: Language code (en/tc/sc) for data format
        district: Optional filter by district name (e.g., 'Tuen Mun'). If not provided, data for all districts will be returned.
    """
    data = fetch_pas_gopc_avg_quota_data(lang)
    if district:
        data = [
            entry for entry in data if entry["District"].lower() == district.lower()
        ]
    return {
        "data": data,
        "last_updated": datetime.now().isoformat(),
        "message": f"Retrieved data for {len(data)} clinics"
        + (f" in {district}" if district else ""),
    }
