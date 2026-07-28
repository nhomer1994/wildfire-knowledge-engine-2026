# src/geospatial/client.py
import datetime
from pystac_client import Client

# Define authoritative public STAC endpoints for Sentinel-2
STAC_CATALOGS = [
    {
        "name": "Microsoft Planetary Computer",
        "url": "https://planetarycomputer.microsoft.com/api/stac/v1",
        "collection": "sentinel-2-l2a"
    },
    {
        "name": "Element 84 AWS Earth Search",
        "url": "https://earth-search.aws.element84.com/v1",
        "collection": "sentinel-2-l2a"
    }
]

def query_sentinel_stac(bbox, days_back=30, max_cloud_cover=15):
    """
    Connects to available public STAC catalogs sequentially to discover
    cloud-free Sentinel-2 imagery. Provides automated failover if an endpoint
    returns malformed data or is blocked.
    """
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_back)
    datetime_range = f"{start_date}/{end_date}"
    
    last_error = None

    for catalog_info in STAC_CATALOGS:
        name = catalog_info["name"]
        url = catalog_info["url"]
        collection = catalog_info["collection"]
        
        print(f"📡 Geospatial Client: Attempting connection to {name}...")
        try:
            # Establish client handshake
            catalog = Client.open(url)
            
            # Execute query search descriptor
            search = catalog.search(
                collections=[collection],
                bbox=bbox,
                datetime=datetime_range,
                query={"eo:cloud_cover": {"lt": max_cloud_cover}}
            )
            
            items = search.item_collection()
            print(f"✅ Failover Success: Located {len(items)} scenes via {name}.")
            return items
            
        except Exception as e:
            print(f"⚠️ Warning: Connection to {name} failed or was blocked. Error: {str(e)}")
            last_error = e
            continue # Try the next catalog in the list

    # If all options in our fallback matrix fail, raise an explicit exception
    raise RuntimeError(
        f"CRITICAL GEOSPATIAL ERROR: All available STAC catalogs failed to parse. "
        f"Last captured error trace: {str(last_error)}"
    )
