"""Utilities for synchronising entities with Notion."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, Mapping, Optional

from shared.logging_config import configure_logging


configure_logging()
logger = logging.getLogger(__name__)


class NotionAPIError(Exception):
    """Base exception for Notion API errors."""

    def __init__(self, message: str, status: int, *, payload: Optional[dict] = None) -> None:
        super().__init__(message)
        self.status = status
        self.payload = payload or {}

    @property
    def is_transient(self) -> bool:
        return self.status in {408, 429, 500, 502, 503, 504}


class NotionObjectNotFound(NotionAPIError):
    """Raised when a Notion resource cannot be located."""

    def __init__(self, message: str = "Notion object not found", *, payload: Optional[dict] = None) -> None:
        super().__init__(message, status=404, payload=payload)


@dataclass
class SyncOutcome:
    """Aggregate information about a synchronisation run."""

    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    missing_mapping: list[str] = field(default_factory=list)
    not_found: list[str] = field(default_factory=list)
    failed: Dict[str, str] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "created": self.created,
            "updated": self.updated,
            "missing_mapping": self.missing_mapping,
            "not_found": self.not_found,
            "failed": self.failed,
        }


class NotionSyncService:
    """Coordinates synchronisation of local entities with Notion pages."""

    def __init__(
        self,
        notion_client: Any,
        *,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        sleep_func: Callable[[float], None] = time.sleep,
    ) -> None:
        configure_logging()
        self.client = notion_client
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._sleep = sleep_func

    def sync_entities(
        self,
        entities: Iterable[Mapping[str, Any]],
        *,
        notion_mappings: Mapping[str, str],
    ) -> SyncOutcome:
        """Synchronise a collection of entities with Notion.

        Args:
            entities: Iterable of objects describing the entities to push to
                Notion. Each entity must contain an ``id`` key.
            notion_mappings: Mapping of entity identifiers to Notion page IDs.

        Returns:
            SyncOutcome summarising the results.
        """

        outcome = SyncOutcome()

        for entity in entities:
            entity_id = str(entity.get("id"))
            if not entity_id or entity_id == "None":
                logger.error("Entity missing identifier; skipping.", extra={"entity": entity})
                continue

            page_id = notion_mappings.get(entity_id)
            if not page_id:
                logger.warning(
                    "No Notion mapping for entity.",
                    extra={"entity_id": entity_id, "status": "missing_mapping"},
                )
                outcome.missing_mapping.append(entity_id)
                continue

            try:
                result = self._upsert_entity(entity, page_id)
            except NotionObjectNotFound:
                logger.warning(
                    "Notion page not found during sync.",
                    extra={"entity_id": entity_id, "page_id": page_id, "status": "not_found"},
                )
                outcome.not_found.append(entity_id)
            except NotionAPIError as exc:
                logger.error(
                    "Failed to sync entity due to Notion API error.",
                    extra={
                        "entity_id": entity_id,
                        "page_id": page_id,
                        "status_code": exc.status,
                        "error": str(exc),
                    },
                    exc_info=True,
                )
                outcome.failed[entity_id] = str(exc)
            except Exception as exc:  # pragma: no cover - defensive safeguard
                logger.exception(
                    "Unexpected error during Notion sync.",
                    extra={"entity_id": entity_id, "page_id": page_id, "status": "unexpected_error"},
                )
                outcome.failed[entity_id] = str(exc)
            else:
                if result == "created":
                    outcome.created.append(entity_id)
                elif result == "updated":
                    outcome.updated.append(entity_id)
                else:
                    outcome.failed[entity_id] = f"Unknown result state: {result}"

        return outcome

    def _upsert_entity(self, entity: Mapping[str, Any], page_id: str) -> str:
        payload = self._build_payload(entity)

        attempts = 0
        while True:
            attempts += 1
            try:
                if page_id == "new":
                    self.client.create_page(payload)
                    logger.info(
                        "Created new Notion page.",
                        extra={"entity_id": entity.get("id"), "status": "created"},
                    )
                    return "created"

                self.client.update_page(page_id, payload)
                logger.info(
                    "Updated existing Notion page.",
                    extra={"entity_id": entity.get("id"), "page_id": page_id, "status": "updated"},
                )
                return "updated"
            except NotionObjectNotFound:
                raise
            except NotionAPIError as exc:
                if exc.is_transient and attempts <= self.max_retries:
                    delay = self.backoff_factor * (2 ** (attempts - 1))
                    logger.warning(
                        "Transient Notion API error; will retry.",
                        extra={
                            "entity_id": entity.get("id"),
                            "page_id": page_id,
                            "status_code": exc.status,
                            "attempt": attempts,
                            "delay": delay,
                        },
                    )
                    self._sleep(delay)
                    continue
                raise

    def _build_payload(self, entity: Mapping[str, Any]) -> Dict[str, Any]:
        """Transform a raw entity dictionary into a Notion payload."""

        title = entity.get("title") or entity.get("name")
        if not title:
            raise ValueError("Entity requires a 'title' or 'name' field for Notion sync")

        properties: Dict[str, Any] = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": str(title),
                        }
                    }
                ]
            }
        }

        description = entity.get("description")
        if description:
            properties["Description"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": str(description),
                        }
                    }
                ]
            }

        status = entity.get("status")
        if status:
            properties["Status"] = {
                "select": {"name": str(status)}
            }

        tags = entity.get("tags")
        if tags:
            properties["Tags"] = {
                "multi_select": [{"name": str(tag)} for tag in tags]
            }

        return {"properties": properties}
