# Notion Sync Runbook

This guide explains how the security agent syncs operational data with Notion while keeping secrets confined to Terraform Cloud.

## Terraform Cloud workspace variables

The GitHub Actions workflows reference the following Terraform Cloud (TFC) workspace **environment variables**. They must be marked as *sensitive* in TFC and never defined directly in this repository.

| Variable name | Purpose |
| --- | --- |
| `NOTION_TOKEN` | Notion internal integration token used for API authentication. |
| `NOTION_INCIDENT_DB_ID` | Database ID for the incident response log. |
| `NOTION_RUNBOOK_DB_ID` | Database ID for automation runbooks or playbooks. |

### Provisioning steps

1. In the TFC workspace backing this project, add the variables above under **Environment Variables** and mark each one as *sensitive*.
2. Generate the `NOTION_TOKEN` from a Notion internal integration that is shared only with the specific databases listed above.
3. Copy the database IDs from Notion (via *Share* → *Copy link* → extract the UUID) and paste them into the matching TFC variable fields.
4. Trigger the next GitHub Actions run; the workflow reads these values through `${{ secrets.* }}` expressions that TFC exposes to the pipeline.

## Least-privilege access

- Create a dedicated Notion internal integration for this workspace. Do **not** reuse a human API token.
- Share only the required databases with the integration. If new content is needed, create a separate database and explicitly share it.
- Limit TFC workspace access so that only the automation account and designated security engineers can view or modify the sensitive variables.

## Rotation policy

- Rotate the `NOTION_TOKEN` at least quarterly or immediately after personnel changes, incident response events, or suspected exposure.
- When rotating, create the new integration token in Notion, update the TFC workspace variable, and revoke the old integration.
- Audit database permissions in Notion during each rotation to confirm that only the automation integration retains access.

## Local dry runs

For contributors who need to execute scripts locally without real credentials:

1. Copy `.env.example` to `.env`.
2. Populate the Notion variable names with placeholder text (e.g., `NOTION_TOKEN=placeholder`) to satisfy local validation.
3. Remember that production values are stored **only** in the Terraform Cloud workspace; never commit real tokens or database IDs to the repository.
