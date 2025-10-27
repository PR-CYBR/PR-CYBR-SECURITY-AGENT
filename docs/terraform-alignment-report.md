# Terraform Schema Alignment Report (A-07)

_Date:_ 2025-03-27

## Overview
- Consolidated Terraform variables under `infra/` to mirror the October 2024 unified schema for PR-CYBR agents.
- Removed deprecated `GLOBAL_*` and `AGENT_COLLAB` variables from code to eliminate drift against the Terraform Cloud workspace definition.
- Introduced placeholder tfvars file to standardize local validation workflows without exposing secrets.
- Hardened the `tfc-sync` workflow to enforce least-privilege secret usage and non-interactive Terraform automation from the `./infra` directory.

## Variable Changes
| Action | Variable Name | Notes |
| ------ | ------------- | ----- |
| Removed | `GLOBAL_DOMAIN` | Legacy global variable outside the authorized schema. |
| Removed | `GLOBAL_ELASTIC_URI` | Legacy global variable outside the authorized schema. |
| Removed | `GLOBAL_GRAFANA_URI` | Legacy global variable outside the authorized schema. |
| Removed | `GLOBAL_KIBANA_URI` | Legacy global variable outside the authorized schema. |
| Removed | `GLOBAL_PROMETHEUS_URI` | Legacy global variable outside the authorized schema. |
| Removed | `GLOBAL_TAILSCALE_AUTHKEY` | Legacy secret relocated to TFC-managed workspaces. |
| Removed | `GLOBAL_TRAEFIK_ACME_EMAIL` | Legacy automation input no longer part of the schema. |
| Removed | `GLOBAL_TRAEFIK_ENTRYPOINTS` | Legacy automation input no longer part of the schema. |
| Removed | `GLOBAL_ZEROTIER_NETWORK_ID` | Legacy secret relocated to TFC-managed workspaces. |
| Removed | `AGENT_COLLAB` | Deprecated token scope superseded by Notion database variables. |
| Added | `AGENT_ACTIONS` | Declared with descriptions and sensitivity metadata. |
| Added | `DOCKERHUB_TOKEN` | Declared with descriptions and sensitivity metadata. |
| Added | `DOCKERHUB_USERNAME` | Declared to align with Docker Hub publishing requirements. |
| Added | `NOTION_DISCUSSIONS_ARC_DB_ID` | Added per October schema update. |
| Added | `NOTION_ISSUES_BACKLOG_DB_ID` | Added per October schema update. |
| Added | `NOTION_KNOWLEDGE_FILE_DB_ID` | Added per October schema update. |
| Added | `NOTION_PAGE_ID` | Added per October schema update. |
| Added | `NOTION_PR_BACKLOG_DB_ID` | Added per October schema update. |
| Added | `NOTION_PROJECT_BOARD_BACKLOG_DB_ID` | Added per October schema update. |
| Added | `NOTION_TASK_BACKLOG_DB_ID` | Added per October schema update. |
| Added | `NOTION_TOKEN` | Added with sensitivity flag to enforce least-privilege. |
| Added | `TFC_TOKEN` | Added with sensitivity flag for Terraform Cloud access. |

## Workflow Updates
- `tfc-sync` now exports `TF_VAR_*` environment variables directly from GitHub Secrets for Terraform runs.
- Added formatting and validation gates before planning/apply stages to guarantee consistent state.
- Each Terraform command is now executed with `-input=false` and `-no-color` to support non-interactive automation and log ingestion.

## Follow-up Validation
- Queue `tfc-sync` and `security-validation` workflows after merge to confirm Terraform Cloud synchronization and policy guardrails succeed with the updated schema.
