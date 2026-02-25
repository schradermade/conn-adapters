from __future__ import annotations

import os

from pydantic import BaseModel, ConfigDict, Field, ValidationError

class ConnectorConfig(BaseModel):
  model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
  
  ingestion_url: str = Field(min_length=1)
  source: str = Field(min_length=1)
  batch_size: int = Field(default=100, ge=1, le=1000)
  
  
def load_config() -> ConnectorConfig:
  raw = {
    'ingestion_url': os.getenv('INGESTION_URL', ''),
    'source': os.getenv('CONNECTOR_SOURCE', 'gdrive'),
    'batch_size': os.getenv('BATCH_SIZE', '100'),
  }
  
  try:
    return ConnectorConfig.model_validate(raw)
  except ValidationError as exc:
    raise RuntimeError(f"Invalid connector configuration: {exc}") from exc