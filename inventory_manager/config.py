from __future__ import annotations
import os
from dotenv import load_dotenv
from typing import Optional

class ConfigLoader:
    _instance: ConfigLoader | None = None

    def __new__(cls) -> "ConfigLoader":
        if cls._instance is None:
            load_dotenv()  # loads .env if present
            cls._instance = super().__new__(cls)
            # set attributes from environment with sensible defaults
            cls._instance.inventory_file = os.getenv("INVENTORY_FILE", "inventory.csv")
            cls._instance.report_file = os.getenv("REPORT_FILE", "outputs/low_stock_report.txt")
            cls._instance.error_log = os.getenv("ERROR_LOG", "outputs/errors.log")
            cls._instance.low_stock_threshold = int(os.getenv("LOW_STOCK_THRESHOLD", "10"))
            cls._instance.download_delay = float(os.getenv("DOWNLOAD_DELAY", "0"))
        return cls._instance

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.getenv(key, default)
