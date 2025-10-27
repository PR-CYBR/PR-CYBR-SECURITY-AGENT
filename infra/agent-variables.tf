#############################################
# PR-CYBR Agent Variables (A-07 Alignment)  #
# These declarations mirror the Terraform   #
# Cloud workspace schema for agent A-07.    #
# Real values are managed in Terraform      #
# Cloud or GitHub Secrets.                  #
#############################################

variable "AGENT_ACTIONS" {
  description = "GitHub token providing least-privilege automation access"
  type        = string
  sensitive   = true
}

variable "DOCKERHUB_TOKEN" {
  description = "Docker Hub access token for container publishing"
  type        = string
  sensitive   = true
}

variable "DOCKERHUB_USERNAME" {
  description = "Docker Hub account username used for publishing"
  type        = string
}

variable "NOTION_DISCUSSIONS_ARC_DB_ID" {
  description = "Notion database ID for the discussions archive ledger"
  type        = string
}

variable "NOTION_ISSUES_BACKLOG_DB_ID" {
  description = "Notion database ID for the issues backlog"
  type        = string
}

variable "NOTION_KNOWLEDGE_FILE_DB_ID" {
  description = "Notion database ID for the knowledge file registry"
  type        = string
}

variable "NOTION_PAGE_ID" {
  description = "Primary Notion workspace page identifier"
  type        = string
}

variable "NOTION_PR_BACKLOG_DB_ID" {
  description = "Notion database ID for the pull-request backlog"
  type        = string
}

variable "NOTION_PROJECT_BOARD_BACKLOG_DB_ID" {
  description = "Notion database ID for the project board backlog"
  type        = string
}

variable "NOTION_TASK_BACKLOG_DB_ID" {
  description = "Notion database ID for the task backlog"
  type        = string
}

variable "NOTION_TOKEN" {
  description = "Notion integration token with least-privilege scopes"
  type        = string
  sensitive   = true
}

variable "TFC_TOKEN" {
  description = "Terraform Cloud user/token for workspace operations"
  type        = string
  sensitive   = true
}
