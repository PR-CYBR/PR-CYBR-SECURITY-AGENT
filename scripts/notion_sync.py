"""Utilities to synchronize GitHub events into a Notion database.

This module provides a ``NotionSync`` class that understands the shape of
GitHub webhook payloads and can upsert the corresponding information into a
Notion database.  The public entry point is the :func:`main` function which can
be used as a command-line interface for local testing.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from notion_client import Client


LOGGER = logging.getLogger(__name__)


def _body_snippet(body: Optional[str], limit: int = 180) -> Optional[str]:
    """Return a truncated snippet of the provided body text.

    Parameters
    ----------
    body:
        The raw text body from the GitHub entity.
    limit:
        Maximum number of characters to include in the snippet.
    """
    if not body:
        return None

    sanitized = body.strip()
    if len(sanitized) <= limit:
        return sanitized
    return f"{sanitized[:limit - 1]}…"


def _coalesce(values: Iterable[Optional[str]]) -> List[str]:
    """Return a list without ``None`` values or empty strings."""
    return [value for value in values if value]


@dataclass
class SyncConfig:
    """Configuration required to communicate with Notion."""

    token: str
    database_id: str
    done_status: str = "Done"

    @classmethod
    def from_env(cls) -> "SyncConfig":
        token = os.environ.get("NOTION_API_KEY")
        database_id = os.environ.get("NOTION_DATABASE_ID")
        done_status = os.environ.get("NOTION_DONE_STATUS", "Done")

        if not token:
            raise EnvironmentError("NOTION_API_KEY must be set")
        if not database_id:
            raise EnvironmentError("NOTION_DATABASE_ID must be set")

        return cls(token=token, database_id=database_id, done_status=done_status)


class NotionSync:
    """Synchronize GitHub entities into a Notion database."""

    reference_property = "GitHub Reference"

    def __init__(self, client: Client, config: SyncConfig) -> None:
        self.client = client
        self.config = config

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def sync_event(self, payload: Dict[str, Any], entity: Optional[str] = None) -> None:
        """Process a GitHub webhook payload.

        Parameters
        ----------
        payload:
            The JSON payload delivered by GitHub.
        entity:
            Optional override forcing the entity handler that should be used.
        """
        entity_type = entity or self._determine_entity_type(payload)
        handler = getattr(self, f"_handle_{entity_type}", None)
        if handler is None:
            raise ValueError(f"Unsupported entity type: {entity_type}")

        LOGGER.debug("Processing %s payload", entity_type)
        handler(payload)

    # ------------------------------------------------------------------
    # Entity handlers
    # ------------------------------------------------------------------
    def _handle_issue(self, payload: Dict[str, Any]) -> None:
        issue = payload.get("issue", {})
        metadata = {
            "id": str(issue.get("number")),
            "title": issue.get("title") or "Untitled Issue",
            "url": issue.get("html_url"),
            "body": _body_snippet(issue.get("body")),
            "status": self._status_from_state(issue.get("state")),
            "assignees": [assignee.get("login") for assignee in issue.get("assignees", [])],
            "labels": [label.get("name") for label in issue.get("labels", [])],
            "entity": "issue",
        }

        if payload.get("action") == "closed":
            metadata["status"] = self.config.done_status

        self._upsert_page(metadata)

    def _handle_pull_request(self, payload: Dict[str, Any]) -> None:
        pull_request = payload.get("pull_request", {})
        metadata = {
            "id": str(pull_request.get("number")),
            "title": pull_request.get("title") or "Untitled Pull Request",
            "url": pull_request.get("html_url"),
            "body": _body_snippet(pull_request.get("body")),
            "status": self._status_from_pull_request(pull_request),
            "assignees": [assignee.get("login") for assignee in pull_request.get("assignees", [])],
            "labels": [label.get("name") for label in pull_request.get("labels", [])],
            "entity": "pull_request",
        }

        action = payload.get("action")
        if action == "closed" or pull_request.get("merged"):
            metadata["status"] = self.config.done_status

        self._upsert_page(metadata)

    def _handle_discussion(self, payload: Dict[str, Any]) -> None:
        discussion = payload.get("discussion", {})
        metadata = {
            "id": str(discussion.get("id")),
            "title": discussion.get("title") or "Untitled Discussion",
            "url": discussion.get("html_url"),
            "body": _body_snippet(discussion.get("body")),
            "status": self._status_from_state(discussion.get("state")),
            "assignees": [],
            "labels": _coalesce([discussion.get("category", {}).get("name")]),
            "entity": "discussion",
        }

        if payload.get("action") == "answered":
            metadata["status"] = self.config.done_status

        self._upsert_page(metadata)

    def _handle_project_card(self, payload: Dict[str, Any]) -> None:
        card = payload.get("project_card", {})
        column_name = payload.get("project_column", {}).get("name")
        metadata = {
            "id": str(card.get("id")),
            "title": card.get("note") or "Project Card",
            "url": card.get("url"),
            "body": _body_snippet(card.get("note")),
            "status": column_name or self._status_from_state(payload.get("action")),
            "assignees": [],
            "labels": [],
            "entity": "project_card",
        }

        if payload.get("action") in {"deleted", "converted"}:
            metadata["status"] = self.config.done_status

        self._upsert_page(metadata)

    def _handle_workflow_run(self, payload: Dict[str, Any]) -> None:
        run = payload.get("workflow_run", {})
        name = run.get("name") or run.get("display_title") or "Workflow Run"
        metadata = {
            "id": str(run.get("id")),
            "title": name,
            "url": run.get("html_url"),
            "body": _body_snippet(run.get("head_commit", {}).get("message")),
            "status": self._status_from_workflow_run(run),
            "assignees": _coalesce([run.get("actor", {}).get("login")]),
            "labels": _coalesce([run.get("event"), run.get("conclusion")]),
            "entity": "workflow_run",
        }

        if run.get("conclusion") in {"success", "failure", "cancelled"}:
            metadata["status"] = self.config.done_status

        self._upsert_page(metadata)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _determine_entity_type(self, payload: Dict[str, Any]) -> str:
        if "pull_request" in payload:
            return "pull_request"
        if "issue" in payload:
            issue = payload.get("issue", {})
            if issue.get("pull_request"):
                return "pull_request"
            return "issue"
        if "discussion" in payload:
            return "discussion"
        if "project_card" in payload:
            return "project_card"
        if "workflow_run" in payload:
            return "workflow_run"
        raise ValueError("Could not determine entity type from payload")

    def _status_from_state(self, state: Optional[str]) -> str:
        if (state or "").lower() == "closed":
            return self.config.done_status
        if (state or "").lower() in {"completed", "resolved"}:
            return self.config.done_status
        return "In Progress"

    def _status_from_pull_request(self, pull_request: Dict[str, Any]) -> str:
        if pull_request.get("merged"):
            return self.config.done_status
        state = pull_request.get("state")
        return self._status_from_state(state)

    def _status_from_workflow_run(self, run: Dict[str, Any]) -> str:
        status = (run.get("status") or "").lower()
        if status in {"completed"}:
            conclusion = (run.get("conclusion") or "").lower()
            if conclusion in {"success", "neutral"}:
                return self.config.done_status
        if status in {"queued", "in_progress"}:
            return "In Progress"
        return "Queued"

    def _properties_from_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        properties: Dict[str, Any] = {
            "Name": {"title": [{"text": {"content": metadata["title"]}}]},
            self.reference_property: {
                "rich_text": [
                    {"text": {"content": f"{metadata['entity']}:{metadata['id']}"}}
                ]
            },
            "GitHub ID": {
                "rich_text": [{"text": {"content": metadata["id"]}}]
            },
            "Status": {"select": {"name": metadata.get("status") or "In Progress"}},
            "Entity": {"select": {"name": metadata.get("entity")}},
        }

        if metadata.get("url"):
            properties["URL"] = {"url": metadata["url"]}

        if metadata.get("body"):
            properties["Description"] = {
                "rich_text": [{"text": {"content": metadata["body"]}}]
            }
        if metadata.get("assignees"):
            properties["Assignees"] = {
                "multi_select": [
                    {"name": assignee}
                    for assignee in metadata.get("assignees", [])
                    if assignee
                ]
            }
        if metadata.get("labels"):
            properties["Labels"] = {
                "multi_select": [
                    {"name": label}
                    for label in metadata.get("labels", [])
                    if label
                ]
            }

        return properties

    def _find_page_by_reference(self, reference: str) -> Optional[str]:
        LOGGER.debug("Searching for existing page with reference %s", reference)
        response = self.client.databases.query(
            database_id=self.config.database_id,
            filter={
                "property": self.reference_property,
                "rich_text": {"equals": reference},
            },
        )
        results = response.get("results", [])
        if not results:
            return None
        return results[0]["id"]

    def _upsert_page(self, metadata: Dict[str, Any]) -> None:
        reference = f"{metadata['entity']}:{metadata['id']}"
        properties = self._properties_from_metadata(metadata)

        page_id = self._find_page_by_reference(reference)
        if page_id:
            LOGGER.info("Updating Notion page %s", page_id)
            self.client.pages.update(page_id=page_id, properties=properties)
        else:
            LOGGER.info("Creating new Notion page for %s", reference)
            self.client.pages.create(
                parent={"database_id": self.config.database_id},
                properties=properties,
            )


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync GitHub event payloads to Notion")
    parser.add_argument(
        "--event",
        required=True,
        help="Path to the GitHub event payload (JSON file)",
    )
    parser.add_argument(
        "--entity",
        choices=["issue", "pull_request", "discussion", "project_card", "workflow_run"],
        help="Override the inferred entity type",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (default: INFO)",
    )
    return parser


def load_event(path: str) -> Dict[str, Any]:
    event_path = Path(path)
    if not event_path.exists():
        raise FileNotFoundError(f"Event payload {path} does not exist")
    with event_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    payload = load_event(args.event)

    config = SyncConfig.from_env()
    client = Client(auth=config.token)
    sync = NotionSync(client=client, config=config)
    sync.sync_event(payload, entity=args.entity)


if __name__ == "__main__":
    main()
