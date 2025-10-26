# Terraform Cloud workspace variable assignments for the PR-CYBR Security Agent
# Replace placeholder values with real data in the Terraform Cloud workspace.

# --- Docker / Registry ---
DOCKERHUB_TOKEN               = "changeme-docker-token"
DOCKERHUB_USERNAME            = "changeme-docker-username"
PR_CYBR_DOCKER_PASS           = "changeme-docker-password"
PR_CYBR_DOCKER_USER           = "changeme-docker-user"

# --- Global Infrastructure URIs ---
GLOBAL_DOMAIN                 = "example.prcybr.local"
GLOBAL_ELASTIC_URI            = "https://elastic.example.prcybr.local"
GLOBAL_GRAFANA_URI            = "https://grafana.example.prcybr.local"
GLOBAL_KIBANA_URI             = "https://kibana.example.prcybr.local"
GLOBAL_PROMETHEUS_URI         = "https://prometheus.example.prcybr.local"

# --- Networking / Security ---
GLOBAL_TAILSCALE_AUTHKEY      = "tskey-xxxxxxxxxxxxxxxxxxxx"
GLOBAL_TRAEFIK_ACME_EMAIL     = "admin@example.prcybr.local"
GLOBAL_TRAEFIK_ENTRYPOINTS    = "web,websecure"
GLOBAL_ZEROTIER_NETWORK_ID    = "abcdef1234567890"

# --- Agent Tokens ---
AGENT_ACTIONS                 = "changeme-agent-actions"
AGENT_COLLAB                  = "changeme-agent-collab"

# --- Notion Workspace ---
NOTION_DISCUSSIONS_ARC_DB_ID      = "notion-db-discussions-arc"
NOTION_ISSUES_BACKLOG_DB_ID       = "notion-db-issues-backlog"
NOTION_KNOWLEDGE_FILE_DB_ID       = "notion-db-knowledge-files"
NOTION_PAGE_ID                    = "notion-page-root"
NOTION_PR_BACKLOG_DB_ID           = "notion-db-pr-backlog"
NOTION_PROJECT_BOARD_BACKLOG_DB_ID = "notion-db-project-board"
NOTION_TASK_BACKLOG_DB_ID         = "notion-db-task-backlog"
NOTION_TOKEN                      = "secret-notion-token"

# --- Automation Secrets ---
TFC_TOKEN                    = "terraform-cloud-token"
GITHUB_TOKEN                 = "github-automation-token"
