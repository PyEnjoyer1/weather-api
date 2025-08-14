import httpx

from .owm_geocoding_service import OWMGeocodingService
from .owm_weather_service import OWMWeatherService



class OWMOrchestrationService:
    def __init__(self, client: httpx.AsyncClient, apikey: str):
        self.geocoding_service = OWMGeocodingService(client, apikey)
        self.weather_service = OWMWeatherService(client, apikey)

    async def get_weather_data(self, city: str):
        coords = await self.geocoding_service.get_coordinates(city)
        weather = await self.weather_service.get_current_weather(coords.lat, coords.lon, city)
        return weather



