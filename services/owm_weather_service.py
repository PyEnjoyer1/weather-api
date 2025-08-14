from pydantic import ValidationError

from config.owm_config import OWMConfig
from models.owm_models import OWMWeatherResponseModel
from utils.logger import get_logger

from exceptions import OWMDataException, OWMDataValidationException

from .owm_base_service import OWMBaseService


logger = get_logger(__name__)


class OWMWeatherService(OWMBaseService):

    def _build_shared_params(self, lat: float, lon: float):
        """Returns a dictionary containing common/shared params across OWM endpoints."""
        return {
            "lat": lat,
            "lon": lon,
            "units": OWMConfig.WeatherConfig.UNITS,
            "lang": OWMConfig.WeatherConfig.LANG
        }

    async def get_current_weather(self, lat: float, lon: float, city=None):
        """
        Get current weather based on the coordinates passed.
        City argument can be passed for logging/debugging purposes.
        """
        city_info = f"{city or f'coordinates ({lat}, {lon})'}"

        logger.info(f"Fetching current weather data for {city_info}.")

        params = self._build_shared_params(lat, lon)

        data = await self._make_request(OWMConfig.CURRENT_WEATHER_URL, params)
        if not data:
            error_msg = f"No current weather data for {city_info}."
            logger.error(error_msg)
            raise OWMDataException(error_msg)

        try:
            result = OWMWeatherResponseModel(**data)
            logger.info(f"Current weather data validated for {city_info}.")
            return result
        except ValidationError as e:
            error_msg = f"Current weather data validation failed for {city_info}: {e}."
            logger.error(error_msg)
            raise OWMDataValidationException(error_msg)
        