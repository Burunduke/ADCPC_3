import yaml
import logging

logger = logging.getLogger(__name__)

class Config:
    def __init__(self, config_path="config.yml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)

        self.data_dir = cfg.get("data_dir", "./data")

        self.mentions = cfg.get("mentions", [])
        if not self.mentions:
            raise ValueError("Пустые запросы")
