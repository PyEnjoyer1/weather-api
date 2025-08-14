

class OWMConfig:
    """Class for storing OWM related configuration."""
    
    CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
    
    MAX_RETRIES = 5 # Number of retries for OWM requests 
    TIMEOUT = 5.0 # Timeout seconds for OWM requests
    
    class GeocodingConfig:
        LIMIT = 1 # Valid range 1-5

    
    class CurrentWeatherConfig:
        UNITS = "metric"
        LANG = "en"
