import pandas as pd
import config

_city_df = None

def _load_city_data():
    global _city_df
    if _city_df is None:
        try:
            _city_df = pd.read_csv(config.POPULATION_DATA)
            _city_df = _city_df.dropna(subset=['population'])
        except FileNotFoundError:
            print(f"Error: City data file not found at {config.POPULATION_DATA}")
            _city_df = pd.DataFrame() # Return empty DataFrame to prevent further errors
        except Exception as e:
            print(f"Error loading city data: {e}")
            _city_df = pd.DataFrame()

def _latlon_to_screen(lat, lon, screen_width, screen_height):
    """Converts latitude and longitude to screen coordinates."""
    # Simple equirectangular projection
    x = int((lon + 180) / 360 * screen_width)
    y = int((-lat + 90) / 180 * screen_height)
    return x, y

def get_city_coordinates(city_name, screen_width, screen_height):
    _load_city_data()
    if _city_df.empty:
        return None, None, None

    # Try to find exact match first
    city_row = _city_df[_city_df['city'].str.lower() == city_name.lower()]

    if city_row.empty:
        # If not found, try city_ascii (for cities with special characters)
        city_row = _city_df[_city_df['city_ascii'].str.lower() == city_name.lower()]

    if not city_row.empty:
        # Take the first match (e.g., highest population if sorted, but not sorted here)
        lat = city_row.iloc[0]['lat']
        lon = city_row.iloc[0]['lng']
        population = city_row.iloc[0]['population']
        x, y = _latlon_to_screen(lat, lon, screen_width, screen_height)
        return x, y, population
    else:
        return None, None, None

if __name__ == "__main__":
    # Example usage
    # Assuming some dummy screen dimensions for testing
    TEST_SCREEN_WIDTH = 1280
    TEST_SCREEN_HEIGHT = 720

    print("Testing city lookup for 'Berlin'...")
    x, y, pop = get_city_coordinates("Berlin", TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT)
    if x is not None:
        print(f"Berlin coordinates: ({x}, {y}), Population: {pop}")
    else:
        print("Berlin not found.")

    print("\nTesting city lookup for 'New York'...")
    x, y, pop = get_city_coordinates("New York", TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT)
    if x is not None:
        print(f"New York coordinates: ({x}, {y}), Population: {pop}")
    else:
        print("New York not found.")

    print("\nTesting city lookup for 'NonExistentCity'...")
    x, y, pop = get_city_coordinates("NonExistentCity", TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT)
    if x is not None:
        print(f"NonExistentCity coordinates: ({x}, {y}), Population: {pop}")
    else:
        print("NonExistentCity not found.")
