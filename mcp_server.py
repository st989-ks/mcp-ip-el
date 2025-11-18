import sys
import os
import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("IPinfo Lite")

api_key = os.getenv('IPINFO_API_KEY', '')
api_url = "https://api.ipinfo.io/lite"

class IPLiteInfo(BaseModel):
    ip: str
    asn: str
    as_name: str
    as_domain: str
    country_code: str
    country: str
    continent_code: str
    continent: str


@mcp.tool()
async def ip_lite(ip: str) -> IPLiteInfo:
    """Get lightweight geolocation and ASN info for IP address"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{api_url}/{ip}?token={api_key}")
        response.raise_for_status()
        data = response.json()

    return IPLiteInfo(
        ip=data.get("ip", ip),
        asn=data.get("asn", ""),
        as_name=data.get("as_name", ""),
        as_domain=data.get("as_domain", ""),
        country_code=data.get("country_code", ""),
        country=data.get("country", ""),
        continent_code=data.get("continent_code", ""),
        continent=data.get("continent", "")
    )


def main_start() -> None:
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    # transport = "see"
    # FastMCP имеет метод sse_app()
    app = mcp.sse_app()
    import uvicorn
    # Это полноценное Starlette приложение
    uvicorn.run(app, host="127.0.0.1", port=5555, log_level="info")
