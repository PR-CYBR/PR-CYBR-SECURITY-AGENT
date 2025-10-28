# Minimal Terraform configuration for PR-CYBR-SECURITY-AGENT
# This provides a valid configuration that the tfc-sync workflow can validate

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

# Minimal resource to make this a valid configuration
resource "null_resource" "agent_placeholder" {
  triggers = {
    agent_name = "pr-cybr-security-agent"
  }
}

# Output the agent configuration status
output "agent_status" {
  value = "PR-CYBR Security Agent configuration validated"
}
