#############################################
# Terraform Variable Schema (PR-CYBR Agents)
#--------------------------------------------
# This schema mirrors the centralized Terraform
# Cloud workspace configuration. Defaults are
# intentionally set to null so local terraform
# plan executions succeed without prompting.
#############################################

variable "AGENT_ID" {
  description = "Unique identifier for this PR-CYBR agent workspace."
  type        = string
  default     = null
}

variable "PR_CYBR_DOCKER_USER" {
  description = "DockerHub user for PR-CYBR managed registries."
  type        = string
  default     = null
}

variable "PR_CYBR_DOCKER_PASS" {
  description = "DockerHub password for PR-CYBR managed registries."
  type        = string
  sensitive   = true
  default     = null
}

variable "DOCKERHUB_USERNAME" {
  description = "Personal DockerHub username for the agent container image."
  type        = string
  default     = null
}

variable "DOCKERHUB_TOKEN" {
  description = "Access token for DockerHub operations."
  type        = string
  sensitive   = true
  default     = null
}

variable "GLOBAL_DOMAIN" {
  description = "Root domain for PR-CYBR hosted services."
  type        = string
  default     = null
}

variable "AGENT_ACTIONS" {
  description = "GitHub Actions automation token."
  type        = string
  sensitive   = true
  default     = null
}

variable "NOTION_TOKEN" {
  description = "Shared Notion integration token."
  type        = string
  sensitive   = true
  default     = null
}

variable "NOTION_DISCUSSIONS_ARC_DB_ID" {
  description = "Notion database ID for discussions archive."
  type        = string
  default     = null
}

variable "NOTION_ISSUES_BACKLOG_DB_ID" {
  description = "Notion database ID for the issues backlog."
  type        = string
  default     = null
}

variable "NOTION_KNOWLEDGE_FILE_DB_ID" {
  description = "Notion database ID for knowledge files."
  type        = string
  default     = null
}

variable "NOTION_PROJECT_BOARD_BACKLOG_DB_ID" {
  description = "Notion database ID for the project board backlog."
  type        = string
  default     = null
}

variable "NOTION_PR_BACKLOG_DB_ID" {
  description = "Notion database ID for the PR backlog."
  type        = string
  default     = null
}

variable "NOTION_TASK_BACKLOG_DB_ID" {
  description = "Notion database ID for the task backlog."
  type        = string
  default     = null
}

variable "NOTION_PAGE_ID" {
  description = "Notion page ID assigned to this agent."
  type        = string
  default     = null
}

variable "TFC_TOKEN" {
  description = "Terraform Cloud API token used for workspace automation."
  type        = string
  sensitive   = true
  default     = null
}
