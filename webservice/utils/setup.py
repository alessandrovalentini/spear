from pydantic import BaseModel
import yaml

class SerialSettings(BaseModel):
    port: str
    baud_rate: int
    timeout: int

class Settings(BaseModel):
    serial: SerialSettings

def load_settings(config_file_path: str ) -> Settings:
    with open(config_file_path, "r") as f:
        config = yaml.safe_load(f)
    return Settings(**config)
