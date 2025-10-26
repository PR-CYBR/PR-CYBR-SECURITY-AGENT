# Notion ↔ GitHub Sync Strategy

## 1. Polling Strategy for Notion Changes

- **Execution model**: Run a scheduled job (e.g., GitHub Action workflow on cron or serverless function on AWS Lambda/Cloudflare Workers) every 5–10 minutes. Alternatively, host a webhook-style listener as a serverless function invoked via an external scheduler (e.g., GitHub Actions `curl`, AWS EventBridge) because Notion does not natively push events.
- **Authentication**: Use the shared Notion integration token stored as a Terraform Cloud environment variable so it is available in all environments without committing secrets.
- **State table**: Maintain a durable store (e.g., DynamoDB table or lightweight Postgres) keyed by Notion page ID with the last known `last_edited_time`, associated GitHub identifiers (issue/PR numbers, repo, branch), and sync status (`pending`, `in-sync`, `error`).
- **Fetch cycle**:
  1. Query Notion databases via the Search or Database Query API filtered by `last_edited_time` greater than the stored cursor.
  2. For each page, read stored GitHub identifiers from dedicated Notion properties (see §3) to correlate with existing artifacts.
  3. Compare Notion status/properties against the stored state to detect transitions (e.g., `Status: Ready for Dev`).
  4. Enqueue derived actions (create issue/PR, comment, close, reopen) into a work queue (e.g., SQS) to be processed idempotently.
- **Idempotency & retries**: Tag every operation with a deterministic `sync_run_id` (`page_id` + ISO timestamp bucket). Persist operation attempts and responses so retries do not create duplicates. When GitHub calls fail (rate limits, network), leave the Notion page flagged `pending` with an error message property updated.
- **Outbound acknowledgement**: After GitHub updates succeed, write back to Notion properties (e.g., `Last Synced At`, `GitHub Status`, `GitHub Issue URL`) and update the state table.

## 2. GitHub-Side Automation

- **Integration choice**: Prefer a GitHub App installed on the organization so we get granular repository permissions (`issues`, `pull_requests`, `contents: read`) and fine-grained webhooks. Use a fall-back Personal Access Token (fine-grained PAT) for repos where App installation is not yet possible.
- **Event processor**:
  - Expose an API endpoint (same serverless stack) that the polling job invokes with desired actions.
  - For **new Notion items** without GitHub IDs, call the GitHub REST API to open an issue (or PR draft) in the target repo, attaching metadata (labels, assignees) defined in Notion.
  - For **status transitions** (e.g., `Status` moves to `Complete`), close the linked issue/PR via PATCH `/issues/{number}` or `/pulls/{number}`.
  - For **reopen events**, PATCH issue/PR state back to `open` when Notion moves from `Complete` to any active state.
  - For **field updates**, sync title, body sections, labels, and project fields when Notion properties change.
  - Log all API calls and responses to CloudWatch/Datadog, linking them with the `sync_run_id` to aid auditing.
- **Permissions & security**:
  - Store App private key / PAT in Terraform Cloud variables and inject at runtime.
  - Enforce rate-limit backoff and queueing so GitHub API quotas are respected.
  - Implement signature verification for inbound GitHub webhook retries (if used) and outbound call audit logging.

## 3. Metadata to Store for Reliable Reconciliation

Store the following fields in both systems now to support future sync guarantees:

| Location | Field | Purpose |
| --- | --- | --- |
| Notion page properties | `GitHub Repository` (e.g., `org/repo`) | Determines target repo without hard-coded mapping. |
| Notion page properties | `GitHub Issue Number` / `PR Number` | Enables direct lookup to update/close items. Leave empty until created, then backfill. |
| Notion page properties | `GitHub Sync Status` (select) | Surface last sync result (`Pending`, `Success`, `Error`). |
| Notion page properties | `Last GitHub Sync At` (date) | Track freshness and support incremental polling window. |
| GitHub issue/PR body | Hidden HTML comment block containing `Notion-Page-ID` and `Last-Notion-Revision` | Allows reverse lookup from GitHub to Notion and detect stale content. |
| GitHub issue/PR body | Visible link to the Notion page | Human-friendly navigation. |
| GitHub project item note / issue comment | `Notion Status Snapshot` JSON | Optional debug payload for auditing mismatches. |
| State table (external) | `page_id`, `last_edited_time`, `sync_run_id`, `github_issue_id`, `github_repo`, `status` | Master record for conflict resolution and replay. |

Additional recommendations:

- Normalize all timestamps to UTC ISO8601.
- Use consistent casing for repository names (`org/repo`) and validate against installation scopes.
- When creating GitHub artifacts, immediately update Notion properties and the state table in a single transaction to avoid orphaned issues.
- Periodically run a reconciliation job that scans GitHub for `<!-- Notion-Page-ID: ... -->` markers to detect items missing in Notion and vice versa.
