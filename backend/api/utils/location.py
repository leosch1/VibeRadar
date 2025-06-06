from geopy.geocoders import Nominatim
from typing import Optional, Dict, Any

class Geolocation:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="viberadar")
        
    def _is_in_sea(self, address: Dict[str, Any]) -> bool:
        """
        Check if the location is in the sea based on address components.
        
        Args:
            address (Dict): The address components from geopy
            
        Returns:
            bool: True if location is in the sea, False otherwise
        """
        # Check for water-related address components
        water_indicators = [
            'ocean', 'sea', 'bay', 'gulf', 'marine', 'coastal', 'offshore'
        ]
        
        # Check all address components for water indicators
        for value in address.values():
            if isinstance(value, str):
                value_lower = value.lower()
                if any(indicator in value_lower for indicator in water_indicators):
                    return True
                    
        return False
        
    def get_from_coords(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get detailed location information from coordinates.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            Dict containing:
                - city_name: Name of the nearest city
                - country_name: Full country name
                - country_code: ISO country code
                - lat: Latitude
                - lon: Longitude
                - is_in_sea: Boolean indicating if location is in the sea
        """
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}", language='en')
            if location is None:
                return {
                    "city_name": "Unknown",
                    "country_name": "Unknown",
                    "country_code": "Unknown",
                    "lat": lat,
                    "lon": lon,
                    "is_in_sea": True  # If we can't get location, assume it's in the sea
                }
                
            address = location.raw.get('address', {})
            is_in_sea = self._is_in_sea(address)
            
            return {
                "city_name": address.get('city') or address.get('town') or address.get('village') or "Unknown",
                "country_name": address.get('country', "Unknown"),
                "country_code": address.get('country_code', "Unknown").upper(),
                "lat": lat,
                "lon": lon,
                "is_in_sea": is_in_sea
            }
            
        except Exception as e:
            print(f"Error getting location info: {e}")
            return {
                "city_name": "Unknown",
                "country_name": "Unknown",
                "country_code": "Unknown",
                "lat": lat,
                "lon": lon,
                "is_in_sea": True  # If there's an error, assume it's in the sea
            }
        
    def get_from_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get location information from a name.
        
        Args:
            name (str): Name of the location
            
        Returns:
            Dict containing:
                - city_name: Name of the nearest city
                - country_name: Full country name
                - lat: Latitude
                - lon: Longitude
        """
        try:
            location = self.geolocator.geocode(name, language='en')
            if location is None:
                return None
                
            return {
                "city_name": location.address.split(",")[0],
                "country_name": location.address.split(",")[-1].strip(),
                "lat": location.latitude,
                "lon": location.longitude
            }
            
        except Exception as e:
            print(f"Error getting location info: {e}")
            return None
            
if __name__ == "__main__":
    geolocation = Geolocation()
    print(geolocation.get_from_coords(47.24247, 8.68376))
    print(geolocation.get_from_name("Dallas, Texas"))
