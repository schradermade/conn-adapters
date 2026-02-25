from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

class SyncRequest(BaseModel):
  model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
  
  type: Literal['full_sync', 'incremental_sync']
  tenant_id: str = Field(min_length=1)
  requested_at: datetime
  

class BaseDocument(BaseModel):
  model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
  
  doc_id: str = Field(min_length=1)
  source: str = Field(min_length=1)
  object_type: str = Field(min_length=1)
  title: str | None = None
  content: str | None = None
  content_pointer: str | None = None
  url: str | None = None
  updated_at: datetime
  source_acl_principals: list[str] = Field(default_factory=list)
  sync_run_id: str = Field(min_length=1)
  checksum: str | None = None
  is_deleted: bool = False
  raw_metadata: dict[str, Any] = Field(default_factory=dict)
  
  @model_validator(mode='after')
  def validate_content_or_pointer(self) -> 'BaseDocument':
    if not self.is_deleted and not (self.content or self.content_pointer):
      raise ValueError('non-deleted documents require content or content_pointer')
    return self