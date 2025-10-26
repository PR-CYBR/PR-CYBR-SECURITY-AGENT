<!--
Updates that need to be made:
1. 
-->

# PR-CYBR-SECURITY-AGENT

## Overview

The **PR-CYBR-SECURITY-AGENT** is a specialized tool designed to enhance the cybersecurity posture of the PR-CYBR ecosystem. It identifies, mitigates, and reports vulnerabilities, ensuring the safety and resilience of interconnected systems.

## Key Features

- **Vulnerability Scanning**: Proactively scans repositories and environments for security issues.
- **Threat Mitigation**: Provides actionable steps to address detected vulnerabilities.
- **Security Auditing**: Validates adherence to best practices across codebases and infrastructure.
- **Integration with CI/CD**: Seamlessly integrates with pipelines to enforce security gates before deployment.
- **Reporting and Alerts**: Generates detailed security reports and sends alerts for critical findings.

## Getting Started

### Prerequisites

- **Git**: For cloning the repository.
- **Python 3.8+**: Required for running scripts.
- **Docker**: Required for containerization and deployment.
- **Access to GitHub Actions**: For automated workflows.

### Local Setup

To set up the `PR-CYBR-SECURITY-AGENT` locally on your machine:

1. **Clone the Repository**

```bash
git clone https://github.com/PR-CYBR/PR-CYBR-SECURITY-AGENT.git
cd PR-CYBR-SECURITY-AGENT
```

2. **Run Local Setup Script**

```bash
./scripts/local_setup.sh
```
_This script will install necessary dependencies and set up the local environment._

3. **Provision the Agent**

```bash
./scripts/provision_agent.sh
```
_This script configures the agent with default settings for local development._

### Cloud Deployment

This repository now uses the Terraform Cloud–GitHub workflow bridge so that all sensitive infrastructure values stay in Terraform Cloud. GitHub Actions only uploads configuration and triggers Terraform Cloud runs.

1. **Configure Terraform Cloud**

   - Create or reuse the Terraform Cloud workspace that manages this agent.
   - Store provider credentials, environment settings, and other secrets as Terraform Cloud workspace variables.
   - Generate a Terraform Cloud user or team API token and save it as the `TFC_TOKEN` GitHub Actions secret.

2. **Provide Repository Metadata**

   - In GitHub, navigate to `Settings` → `Secrets and variables` → `Actions` → `Variables`.
   - Define the following repository variables so the workflows can target the correct workspace:
     - `TF_CLOUD_ORGANIZATION`
     - `TF_WORKSPACE`
     - `TF_CONFIG_DIRECTORY` (optional, defaults to the repository root when unset)

3. **Terraform Cloud Workflows**

   - `.github/workflows/terraform-cloud-speculative.yml` uploads configuration and starts speculative runs for pull requests targeting `main` and for pushes to the automation branches (`codex`, `agents`).
   - `.github/workflows/terraform-cloud-apply.yml` uploads configuration and requests an apply run when changes land on `main`.

With this bridge in place, Terraform Cloud remains the system of record for secrets while GitHub Actions orchestrates run creation.

## Integration

The `PR-CYBR-SECURITY-AGENT` integrates with other PR-CYBR agents to provide comprehensive security coverage. It communicates with:

- **PR-CYBR-CI-CD-AGENT**: Integrates into the CI/CD pipeline to perform security scans before deployments.
- **PR-CYBR-BACKEND-AGENT** and **PR-CYBR-FRONTEND-AGENT**: Scans codebases and applications for vulnerabilities.
- **PR-CYBR-INFRASTRUCTURE-AGENT**: Ensures infrastructure configurations meet security standards.
- **PR-CYBR-MGMT-AGENT**: Reports security status and incidents for oversight and decision-making.

## Usage

- **Development**

  - Start the security tools:

```bash
python setup.py develop
```

  - Configure scanning parameters in the `config/` directory.

- **Testing**

  - Run security tests:

```bash
python -m unittest discover tests
```

- **Building for Production**

  - Build the agent for production use:

```bash
python setup.py install
```

## License

This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for details.

---

For more information, refer to the [PR-CYBR Documentation](https://github.com/PR-CYBR/PR-CYBR-SECURITY-AGENT/Wiki) or contact the PR-CYBR team.
