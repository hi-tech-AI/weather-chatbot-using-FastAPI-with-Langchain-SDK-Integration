import os
from typing import Tuple, Optional
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

load_dotenv()


class GeoLocation:
    def __init__(self) -> None:
        """Initialize the GeoLocation service with the OpenCage API key."""
        self.opencage_api_key = self._load_opencage_api_key()
        self.geocoder = OpenCageGeocode(self.opencage_api_key)

    @staticmethod
    def _load_opencage_api_key() -> str:
        """Load the OpenCage API key from environment variables."""
        api_key = os.getenv("OPENCAGE_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENCAGE_API_KEY not found in environment variables."
            )
        return api_key

    def get_geo_info(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Get geographical information for a given location.

        Args:
            location: The name or description of the location to geocode.

        Returns:
            A tuple containing the latitude and longitude of the location,
            or None if the location could not be resolved.
        """
        if not location:
            raise ValueError("Location must be provided.")

        try:
            result = self.geocoder.geocode(location)
            if not result:
                raise ValueError("Location not found in OpenCage results.")

            latitude = result[0]["geometry"]["lat"]
            longitude = result[0]["geometry"]["lng"]
            return latitude, longitude

        except Exception as e:
            print(f"An error occurred while fetching geo info: {e}")
            return None
