"""
Module for fetching average number of general outpatient clinic quotas
for the preceding 4 weeks across districts in Hong Kong from Hospital Authority.
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import Field
from typing_extensions import Annotated
from hkopenai_common.json_utils import fetch_json_data





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


def _get_pas_gopc_avg_quota(
    lang: Optional[str] = "en", district: Optional[str] = ""
) -> Dict:
    """Get average number of general outpatient clinic quotas for the preceding 4 weeks

    Args:
        lang: Language code (en/tc/sc) for data format
        district: Optional filter by district name (e.g., 'Tuen Mun'). If not provided, data for all districts will be returned.
    """
    url = (
        f"https://www.ha.org.hk/pas_gopc/pas_gopc_avg_quota_pdf/g0_9uo7a_p-{lang}.json"
    )
    data = fetch_json_data(url)
    if "error" in data:
        return {"type": "Error", "error": data["error"]}
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
