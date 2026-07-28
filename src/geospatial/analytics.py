# src/geospatial/analytics.py
import numpy as np
import odc.stac
import planetary_computer  # 🔑 Added for automated URL token signatures
from src.geospatial.client import query_sentinel_stac

def calculate_burn_metrics(bbox, days_back=30):
    """
    Streams signed satellite pixel matrices over a bounding box,
    isolates key spectral bands, and calculates structural burn scars.
    """
    scenes = query_sentinel_stac(bbox=bbox, days_back=days_back)
    
    if len(scenes) == 0:
        return {
            "status": "No clear imagery found for this date range.",
            "mean_nbr": None,
            "burn_severity_index": "Unknown"
        }
    
    print("📥 Analytics Engine: Signing asset collections to unlock storage links...")
    # 🚀 Crucial Fix: Intercept items and inject active Azure SAS tokens [1.1]
    signed_scenes = planetary_computer.sign_item_collection(scenes)
    
    print("📥 Analytics Engine: Streaming specific pixel arrays from cloud files...")
    try:
        ds = odc.stac.load(
            signed_scenes,  # Pass the signed structures here
            bands=["B08", "B12"], 
            bbox=bbox,
            chunks={"x": 256, "y": 256}
        )
        nir = ds.B08.astype(float)
        swir = ds.B12.astype(float)
    except Exception:
        # Fallback to alternative band names if using an unauthenticated mirror catalog
        ds = odc.stac.load(scenes, bands=["nir", "swir22"], bbox=bbox, chunks={"x": 256, "y": 256})
        nir = ds.nir.astype(float)
        swir = ds.swir22.astype(float)

    print("🧮 Analytics Engine: Computing Normalized Burn Ratio matrix arrays...")
    nbr_matrix = (nir - swir) / (nir + swir)
    latest_layer = nbr_matrix.isel(time=-1)
    
    mean_nbr_val = float(latest_layer.mean(skipna=True).values)
    
    if mean_nbr_val < -0.1:
        severity = "High-severity fire scar detected"
    elif mean_nbr_val < 0.1:
        severity = "Moderate-severity burn / degraded canopy"
    else:
        severity = "Healthy unburned vegetation canvas"
        
    return {
        "status": f"Analysed snapshot from {len(scenes)} tracking layers",
        "mean_nbr": round(mean_nbr_val, 4),
        "burn_severity_index": severity
    }
