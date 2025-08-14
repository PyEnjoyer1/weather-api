from pydantic import ValidationError

from exceptions import OWMDataValidationException, OWMDataException

from config.owm_config import OWMConfig
from models.owm_models import OWMGeocodingResponseModel
from utils.logger import get_logger

from .owm_base_service import OWMBaseService


logger = get_logger(__name__)


class OWMGeocodingService(OWMBaseService):
    
    async def get_coordinates(self, city: str):
        """Get coordinates for a city. Returns the most relevant match."""
        if not city:
            raise ValueError("City name must be provided.")
        normalized_city = city.strip().lower()

        logger.info(f"Fetching coordinates for city: {city}.")

        data = await self._make_request(
            OWMConfig.GEOCODING_URL,
            params={"q": normalized_city, "limit": OWMConfig.GeocodingConfig.LIMIT}
        )
        if not data:
            error_msg = f"No geocoding data found for city: {city}"
            logger.warning(error_msg)
            raise OWMDataException(error_msg)
            
        try:
            result = OWMGeocodingResponseModel(**data[0])
            logger.info(f"Added coordinates ({result.lat}, {result.lon}) for city: {city}.")
            return result
        except ValidationError as e:
            error_msg = f"Geocoding validation failed for city: {city}. Error: {e}"
            logger.error(error_msg)
            raise OWMDataValidationException(error_msg)


            



        
        
        
        


        

        

