from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from .base import BaseDocument, SyncRequest


class GoogleDriveSyncRequest(SyncRequest):
    source: Literal["gdrive"] = "gdrive"


class GoogleDriveDocument(BaseDocument):
    source: Literal["gdrive"] = "gdrive"
    object_type: Literal["file", "folder"]

    drive_id: str | None = None
    file_id: str | None = Field(default=None, min_length=1)
    mime_type: str | None = None
    owner_email: str | None = None

    @model_validator(mode="after")
    def validate_drive_ids(self) -> "GoogleDriveDocument":
        if self.object_type == "file" and not self.file_id:
            raise ValueError("file objects require file_id")
        return self
