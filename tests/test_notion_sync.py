import logging
import unittest
from unittest.mock import MagicMock

from agent_logic.notion_sync import (
    NotionAPIError,
    NotionObjectNotFound,
    NotionSyncService,
)


class NotionSyncServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = MagicMock()
        self.service = NotionSyncService(self.client, sleep_func=lambda _: None)

    def test_build_payload_includes_core_fields(self) -> None:
        entity = {
            "id": "1",
            "title": "Test Entity",
            "description": "Important details",
            "status": "Active",
            "tags": ["alpha", "beta"],
        }

        payload = self.service._build_payload(entity)

        self.assertIn("properties", payload)
        properties = payload["properties"]
        self.assertEqual(properties["Name"]["title"][0]["text"]["content"], "Test Entity")
        self.assertEqual(properties["Description"]["rich_text"][0]["text"]["content"], "Important details")
        self.assertEqual(properties["Status"]["select"]["name"], "Active")
        self.assertEqual({tag["name"] for tag in properties["Tags"]["multi_select"]}, {"alpha", "beta"})

    def test_sync_entities_updates_existing_page(self) -> None:
        entities = [{"id": "42", "title": "Existing"}]
        mappings = {"42": "page-42"}

        outcome = self.service.sync_entities(entities, notion_mappings=mappings)

        self.client.update_page.assert_called_once()
        self.assertEqual(outcome.updated, ["42"])
        self.assertEqual(outcome.created, [])

    def test_sync_entities_creates_new_page_when_mapping_indicates_new(self) -> None:
        entities = [{"id": "100", "title": "Create Me"}]
        mappings = {"100": "new"}

        outcome = self.service.sync_entities(entities, notion_mappings=mappings)

        self.client.create_page.assert_called_once()
        self.assertEqual(outcome.created, ["100"])

    def test_sync_entities_handles_missing_mapping(self) -> None:
        entities = [{"id": "55", "title": "Missing"}]

        outcome = self.service.sync_entities(entities, notion_mappings={})

        self.assertEqual(outcome.missing_mapping, ["55"])
        self.client.update_page.assert_not_called()
        self.client.create_page.assert_not_called()

    def test_sync_entities_handles_notion_not_found(self) -> None:
        entities = [{"id": "88", "title": "Ghost"}]
        mappings = {"88": "page-88"}

        self.client.update_page.side_effect = NotionObjectNotFound()

        outcome = self.service.sync_entities(entities, notion_mappings=mappings)

        self.assertEqual(outcome.not_found, ["88"])

    def test_sync_entities_retries_transient_errors(self) -> None:
        entities = [{"id": "17", "title": "Retry"}]
        mappings = {"17": "page-17"}

        side_effects = [NotionAPIError("timeout", 429), None]

        def update_page(_, __):
            result = side_effects.pop(0)
            if result is not None:
                raise result
            return result

        self.client.update_page.side_effect = update_page

        outcome = self.service.sync_entities(entities, notion_mappings=mappings)

        self.assertEqual(outcome.updated, ["17"])
        self.assertEqual(self.client.update_page.call_count, 2)

    def test_sync_entities_captures_api_error_and_continues(self) -> None:
        entities = [
            {"id": "alpha", "title": "Alpha"},
            {"id": "beta", "title": "Beta"},
        ]
        mappings = {"alpha": "page-a", "beta": "page-b"}

        self.client.update_page.side_effect = [NotionAPIError("boom", 400), None]

        outcome = self.service.sync_entities(entities, notion_mappings=mappings)

        self.assertIn("alpha", outcome.failed)
        self.assertEqual(outcome.updated, ["beta"])


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    unittest.main()
