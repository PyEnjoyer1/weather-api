import asyncio
import httpx

from fastapi import status

from exceptions import OWMAPIException, OWMDataException
from config.owm_config import OWMConfig
from utils.logger import get_logger

from fibonacci import fibonacci


logger = get_logger(__name__)


class OWMBaseService:
    
    def __init__(self, client: httpx.AsyncClient, apikey: str):
        if not apikey:
            error_msg = f"No OWM api key provided for {self.__class__.__name__}."
            logger.debug(error_msg)
            raise ValueError(error_msg)
        
        self.apikey = apikey
        self.client = client
        logger.info(f"Successfully initialized {self.__class__.__name__}.")

    async def _make_request(self, url: str, params: dict, max_retries=OWMConfig.MAX_RETRIES):
        request_info = f"Endpoint: {url}. Params: {params}"
        logger.info(f"Making request to OWM. {request_info}")

        retry_delays = fibonacci(start=1, length=OWMConfig.MAX_RETRIES + 1)
        for retry in range(max_retries):
            try:
                logger.info(f"Attempt: {retry}.")

                params = {**params, "appid": self.apikey}

                response = await self.client.get(url=url, params=params, timeout=OWMConfig.TIMEOUT)
                response.raise_for_status()

                logger.info(f"OWM request: {request_info} successful after {retry} attempt.")

                try:
                    return response.json()
                except ValueError as e:
                    error_msg = f"Malformed JSON returned: Request: {request_info}. Error: {e}"
                    logger.warning(error_msg) 
                    raise OWMDataException(error_msg)
            except httpx.HTTPStatusError as e:
                if not self._is_retryable_error(e):
                    error_msg = f"Client side error: {e} - {request_info}."
                    logger.error(error_msg)
                    raise OWMAPIException(error_msg, status_code=e.response.status_code, original_exception=e)
                    
                if retry == max_retries - 1:
                    error_msg = f"OWM request: {request_info} failed after {max_retries}. Error: {e}"
                    logger.error(error_msg)
                    raise OWMAPIException(error_msg, status_code=e.response.status_code, original_exception=e)

                logger.warning(
                    f"OWM request: {request_info} failed. Attempt ({retry + 1}/{max_retries}). Error: {e}"
                    )
                await asyncio.sleep(retry_delays[retry])

    def _is_retryable_error(self, error: httpx.HTTPStatusError):
        """
        Check if the HTTP error should be retried.
        Only server errors (5xx) and rate limits (429) are eligible for retries.
        """
        return (
            error.response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR or 
            error.response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        )
            



