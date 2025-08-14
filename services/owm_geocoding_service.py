from pydantic import ValidationError

from exceptions import OWMDataValidationException, OWMDataException

from config.owm_config import OWMConfig
from models.owm_models import OWMGeocodingResponseModel
from utils.logger import get_logger

from .owm_base_service import OWMBaseService


logger = get_logger(__name__)


class OWMGeocodingService(OWMBaseService):
    
    async def get_coordinates(self, city: str, multiple_results: bool = False):
        """
        Get coordinates for a city.
        Returns only the most relevant match if multiple_results flag is set to False,
        all results otherwise (capped at 5).
        """
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
        
        result = []
        for item in data:
            try:
                coords = OWMGeocodingResponseModel(**item)
                result.append(coords)
                logger.info(f"Added coordinates ({coords.lat}, {coords.lon}) for city: {city}.")
            except ValidationError as e:
                logger.warning(f"Invalid geocoding item {item}. Validation failed: {e}.")
                continue

        if not result:
            error_msg = f"No valid geocoding results returned for {city}."
            logger.error(error_msg)
            raise OWMDataValidationException(error_msg)

        logger.info(f"{len(result)} geocoding items passed validation for {city}.")

        # Return only the first/most relevant result if multiple_results flag is False, all results otherwise.
        return result[0] if not multiple_results else result 
    

            



        
        
        
        


        

        

