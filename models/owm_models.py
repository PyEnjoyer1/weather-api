from typing import Optional

from pydantic import BaseModel


class OWMGeocodingResponseModel(BaseModel):
    """Model for storing responses from OWM Geocoding API."""
    name: str
    lat: float
    lon: float
    country: str
    state: Optional[str]


class CoordModel(BaseModel):
    """Model for storing coordinates from OpenWeatherMap response."""
    lat: float
    lon: float


class WeatherModel(BaseModel):
    """Model for storing weather info from OpenWeatherMap response."""
    main: str
    description: str
    icon: str


class MainModel(BaseModel):
    """Model for storing temperature info from OpenWeatherMap response."""
    temp: float
    temp_max: float
    temp_min: float
    feels_like: float
    humidity: float


class SysModel(BaseModel):
    """Model for storing sys info from OpenWeatherMap response."""
    country: str
    sunrise: int
    sunset: int


class OWMWeatherResponseModel(BaseModel):
    """Model for storing responses from OWM Weather API."""
    coord: CoordModel
    weather: list[WeatherModel]
    main: MainModel
    sys: SysModel
    timezone: int



    





