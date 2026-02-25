from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ConnectorAdapter(ABC):
    """Source adapter interface implemented by each connector provider."""

    source: str

    @abstractmethod
    def fetch_full(self, *, tenant_id: str, cursor: str | None = None) -> list[dict[str, Any]]:
        """Fetch full source objects for a tenant."""

    @abstractmethod
    def fetch_incremental(self, *, tenant_id: str, cursor: str) -> list[dict[str, Any]]:
        """Fetch changed source objects since cursor."""

    @abstractmethod
    def normalize(self, *, raw_object: dict[str, Any], sync_run_id: str) -> dict[str, Any]:
        """Normalize raw source object to base normalized document contract."""

    @abstractmethod
    def emit_tombstone(self, *, object_id: str, sync_run_id: str) -> dict[str, Any]:
        """Build tombstone payload for removed/inaccessible source object."""

    @abstractmethod
    def checkpoint_commit(self, *, tenant_id: str, cursor: str) -> dict[str, Any]:
        """Build checkpoint payload after successful sync segment."""
