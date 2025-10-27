#############################################
# PR-CYBR Agent Terraform Bootstrap
#--------------------------------------------
# This file provides the baseline Terraform
# configuration shared by every PR-CYBR agent.
# Environment-specific values are sourced from
# Terraform Cloud workspace variables.
#############################################

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

# Locals expose the variables consumed by downstream
# modules and workflows. They intentionally mirror the
# Terraform Cloud workspace variables so that `terraform
# plan` can execute without prompting for user input.
locals {
  agent = {
    id             = var.AGENT_ID
    notion_page_id = var.NOTION_PAGE_ID
    actions_token  = var.AGENT_ACTIONS
  }

  dockerhub = {
    username = var.DOCKERHUB_USERNAME
    token    = var.DOCKERHUB_TOKEN
  }

  registry = {
    username = var.PR_CYBR_DOCKER_USER
    password = var.PR_CYBR_DOCKER_PASS
  }

  notion = {
    token                       = var.NOTION_TOKEN
    discussions_arc_database_id = var.NOTION_DISCUSSIONS_ARC_DB_ID
    issues_backlog_database_id  = var.NOTION_ISSUES_BACKLOG_DB_ID
    knowledge_file_database_id  = var.NOTION_KNOWLEDGE_FILE_DB_ID
    project_board_database_id   = var.NOTION_PROJECT_BOARD_BACKLOG_DB_ID
    pr_backlog_database_id      = var.NOTION_PR_BACKLOG_DB_ID
    task_backlog_database_id    = var.NOTION_TASK_BACKLOG_DB_ID
    page_id                     = var.NOTION_PAGE_ID
  }

  platform = {
    global_domain = var.GLOBAL_DOMAIN
  }
}

# A placeholder null_resource is kept so that Terraform
# consistently evaluates the locals during validation and
# plan phases. No real infrastructure is managed from this
# repository; TFC workspaces orchestrate downstream modules.
resource "null_resource" "agent_context" {
  triggers = {
    agent_id       = local.agent.id != null ? local.agent.id : ""
    notion_page_id = local.agent.notion_page_id != null ? local.agent.notion_page_id : ""
    global_domain  = local.platform.global_domain != null ? local.platform.global_domain : ""
    dockerhub_user = local.dockerhub.username != null ? local.dockerhub.username : ""
    registry_user  = local.registry.username != null ? local.registry.username : ""
  }
}
