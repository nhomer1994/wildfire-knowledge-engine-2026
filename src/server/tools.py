# src/server/tools.py
from mcp.server.fastmcp import FastMCP
from src.geospatial.analytics import calculate_burn_metrics

# 🤖 Create a named Model Context Protocol server instance
mcp = FastMCP("Wildfire-EO-Intelligence")

@mcp.tool()
def calculate_regional_burn_severity(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> str:
    """
    Calculates the mean Normalized Burn Ratio (NBR) from Sentinel-2 
    satellite imagery over a bounding box to assess recent 2026 fire damage.
    Negative values indicate severe burn scars.
    """
    bbox = [min_lon, min_lat, max_lon, max_lat]
    print(f"🛰️ MCP Server: Tool execution triggered for BBox {bbox}")
    
    try:
        results = calculate_burn_metrics(bbox=bbox, days_back=30)
        
        output_string = (
            f"--- SATELLITE ANALYTICS REPORT ---\n"
            f"Processing Status: {results['status']}\n"
            f"Mean Calculated NBR: {results['mean_nbr']}\n"
            f"Environmental Assessment: {results['burn_severity_index']}\n"
            f"----------------------------------"
        )
        return output_string
        
    except Exception as e:
        return f"CRITICAL TOOL ERROR: Failed to compute satellite matrices: {str(e)}"

if __name__ == "__main__":
    # Start the server using standard Input/Output transport streams (stdio)
    mcp.run()
