from pydantic_settings import BaseSettings

class ValidatorSettings(BaseSettings):
    # == Scoring ==
    iteration_interval: int = 800  # Set according to your desired frequency
    max_allowed_weights: int = 400  # Adjust based on subnet settings
