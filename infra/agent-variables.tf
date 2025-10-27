#############################################
# Variable Outputs
#--------------------------------------------
# These outputs are consumed by automation
# pipelines (e.g., tfc-sync) to mirror Terraform
# Cloud workspace variables into GitHub Actions
# secrets without duplicating data in-repo.
#############################################

output "agent" {
  description = "Core metadata describing the agent."
  value       = local.agent
  sensitive   = true
}

output "dockerhub" {
  description = "DockerHub credentials used for publishing images."
  value       = local.dockerhub
  sensitive   = true
}

output "registry" {
  description = "PR-CYBR managed registry credentials."
  value       = local.registry
  sensitive   = true
}

output "notion" {
  description = "Notion integration credentials and database IDs."
  value       = local.notion
  sensitive   = true
}

output "platform" {
  description = "Global platform configuration shared across agents."
  value       = local.platform
}
