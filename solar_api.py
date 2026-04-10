import requests
import json

API_KEY = "AIzaSyDMpo4xVLbEj0G1l_9WaaDW4kTpIg7TZaw"
BASE_URL = "https://solar.googleapis.com/v1"


def get_building_insights(latitude: float, longitude: float, quality: str = "HIGH") -> dict:
    """Fetch solar building insights for a given location."""
    url = f"{BASE_URL}/buildingInsights:findClosest"
    params = {
        "location.latitude": latitude,
        "location.longitude": longitude,
        "requiredQuality": quality,
        "key": API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def summarize_solar_potential(data: dict) -> None:
    """Print a readable summary of solar potential data."""
    sp = data.get("solarPotential", {})
    center = data.get("center", {})

    print(f"Building: {data.get('name')}")
    print(f"Location: {center.get('latitude')}, {center.get('longitude')}")
    print(f"Imagery Date: {data.get('imageryDate')}")
    print()
    print("--- Solar Potential ---")
    print(f"Max panels:               {sp.get('maxArrayPanelsCount')}")
    print(f"Max array area (m²):      {sp.get('maxArrayAreaMeters2'):.1f}")
    print(f"Max sunshine hrs/year:    {sp.get('maxSunshineHoursPerYear'):.1f}")
    print(f"Carbon offset (kg/MWh):   {sp.get('carbonOffsetFactorKgPerMwh'):.2f}")

    configs = sp.get("solarPanelConfigs", [])
    if configs:
        best = configs[-1]
        print()
        print("--- Best Panel Config ---")
        print(f"Panels:                   {best.get('panelsCount')}")
        print(f"Annual energy (kWh):      {best.get('yearlyEnergyDcKwh'):.1f}")


if __name__ == "__main__":
    # Example: Google HQ area (Palo Alto)
    lat, lng = 37.4450, -122.1390

    print(f"Fetching solar data for ({lat}, {lng})...\n")
    data = get_building_insights(lat, lng)

    # Save raw response
    with open("building_insights.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Raw response saved to building_insights.json\n")

    summarize_solar_potential(data)
