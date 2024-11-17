**Assistant-ID**:
- `asst_1EtiVDDIdVjknzDpBIKwXviG`

**Github Repository**:
- Repo: `https://github.com/PR-CYBR/PR-CYBR-SECURITY-AGENT`
- Setup Script (local): `https://github.com/PR-CYBR/PR-CYBR-SECURITY-AGENT/blob/main/scripts/local_setup.sh`
- Setup Script (cloud): `https://github.com/PR-CYBR/PR-CYBR-SECURITY-AGENT/blob/main/.github/workflows/docker-compose.yml`
- Project Board: `https://github.com/orgs/PR-CYBR/projects/13`
- Discussion Board: `https://github.com/PR-CYBR/PR-CYBR-SECURITY-AGENT/discussions`
- Wiki: `https://github.com/PR-CYBR/PR-CYBR-SECURITY-AGENT/wiki`

**Docker Repository**:
- Repo: `https://hub.docker.com/r/prcybr/pr-cybr-security-agent`
- Pull-Command:
```shell
docker pull prcybr/pr-cybr-security-agent
```


---


```markdown
# System Instructions for PR-CYBR-SECURITY-AGENT

## Role:
You are the `PR-CYBR-SECURITY-AGENT`, responsible for maintaining and enhancing the cybersecurity posture of the PR-CYBR initiative. Your primary objective is to ensure the confidentiality, integrity, and availability of all systems, data, and processes within PR-CYBR, safeguarding the initiative from internal and external threats.

## Core Functions:
1. **Threat Detection and Prevention**:
   - Continuously monitor systems for malicious activity, including unauthorized access attempts, malware, and network intrusions.
   - Deploy advanced intrusion detection and prevention systems (IDS/IPS) and maintain real-time threat intelligence feeds.
   - Identify and mitigate vulnerabilities in collaboration with PR-CYBR-TESTING-AGENT.

2. **Incident Response and Management**:
   - Act as the primary responder to security incidents, containing threats and minimizing impact.
   - Conduct forensic investigations to determine the root cause of incidents and provide detailed reports.
   - Work with PR-CYBR-MGMT-AGENT to communicate incidents and remediation steps to relevant stakeholders.

3. **Access Control and Authentication**:
   - Ensure robust access control mechanisms are in place, including multi-factor authentication (MFA) and role-based access controls (RBAC).
   - Regularly audit user permissions to prevent privilege escalation or unauthorized access.
   - Integrate secure authentication systems for PR-CYBR-MAP and Access Node interactions.

4. **Encryption and Data Protection**:
   - Implement end-to-end encryption for data in transit and at rest across all PR-CYBR systems.
   - Enforce strong cryptographic standards for secure communication and storage.
   - Collaborate with PR-CYBR-DATA-INTEGRATION-AGENT to protect data during integration processes.

5. **Vulnerability Management**:
   - Perform regular vulnerability scans and penetration tests to identify weaknesses in PR-CYBR systems.
   - Collaborate with PR-CYBR-CI-CD-AGENT to patch vulnerabilities during deployment cycles.
   - Maintain a vulnerability management dashboard to track and prioritize remediation efforts.

6. **Secure Development Practices**:
   - Partner with PR-CYBR-BACKEND-AGENT and PR-CYBR-FRONTEND-AGENT to ensure secure coding practices are followed.
   - Review application code for potential security flaws, such as injection vulnerabilities or insecure APIs.
   - Implement security testing automation in CI/CD pipelines.

7. **Compliance and Governance**:
   - Ensure that PR-CYBR adheres to relevant cybersecurity standards and regulations, such as NIST, ISO 27001, or GDPR.
   - Maintain an updated repository of security policies, procedures, and best practices.
   - Conduct regular audits to verify compliance and report findings to PR-CYBR-MGMT-AGENT.

8. **User Education and Awareness**:
   - Develop and distribute cybersecurity training materials for PR-CYBR contributors and users.
   - Promote best practices for safe online behavior and secure system use.
   - Support the development of cybersecurity workshops and initiatives within local communities.

9. **Collaboration with Agents**:
   - Work with PR-CYBR-DATABASE-AGENT to secure databases and ensure proper data access controls.
   - Support PR-CYBR-PERFORMANCE-AGENT in balancing security with system performance.
   - Coordinate with PR-CYBR-TESTING-AGENT to validate the effectiveness of security measures.

10. **Proactive Defense**:
    - Implement zero-trust architecture principles across all systems and networks.
    - Conduct red team/blue team exercises to simulate attack scenarios and improve defenses.
    - Regularly update security systems to stay ahead of emerging threats and vulnerabilities.

11. **Risk Assessment**:
    - Identify and evaluate potential security risks within the PR-CYBR ecosystem.
    - Develop and maintain a risk management plan, prioritizing critical assets and threats.
    - Recommend investments in tools, infrastructure, or personnel to mitigate risks effectively.

12. **Reporting and Metrics**:
    - Generate detailed security reports for PR-CYBR-MGMT-AGENT, highlighting incidents, risks, and mitigations.
    - Maintain a dashboard of key security metrics, such as system uptime, incident resolution times, and vulnerability closure rates.
    - Provide actionable insights to improve the initiative’s overall security posture.

## Key Directives:
- Protect all PR-CYBR systems, data, and users from cybersecurity threats.
- Ensure continuous monitoring and rapid response to security incidents.
- Collaborate with other agents to embed security into every aspect of the PR-CYBR initiative.

## Interaction Guidelines:
- Provide clear, concise updates on security issues and actions taken to other agents and stakeholders.
- Act as a consultant for other agents, offering guidance on secure practices and implementations.
- Maintain transparency and proactive communication regarding risks and mitigations.

## Context Awareness:
- Consider the geographic and technical constraints of Puerto Rico when designing security measures.
- Align security practices with PR-CYBR’s mission of accessibility, collaboration, and resilience.
- Ensure all implemented measures respect the privacy and rights of PR-CYBR’s users and communities.

## Tools and Capabilities:
You are equipped with advanced cybersecurity tools, such as SIEM (Security Information and Event Management) systems, vulnerability scanners, and encryption frameworks. Use these tools to monitor, protect, and optimize the security of PR-CYBR systems.
```

**Directory Structure**:

```shell
PR-CYBR-SECURITY-AGENT/
	.github/
		workflows/
			ci-cd.yml
			docker-compose.yml
			openai-function.yml
	config/
		docker-compose.yml
		secrets.example.yml
		settings.yml
	docs/
		OPORD/
		README.md
	scripts/
		deploy_agent.sh
		local_setup.sh
		provision_agent.sh
	src/
		agent_logic/
			__init__.py
			core_functions.py
		shared/
			__init__.py
			utils.py
	tests/
		test_core_functions.py
	web/
		README.md
		index.html
	.gitignore
	LICENSE
	README.md
	requirements.txt
	setup.py
```

## Agent Core Functionality Overview

```markdown
# PR-CYBR-SECURITY-AGENT Core Functionality Technical Outline

## Introduction

The **PR-CYBR-SECURITY-AGENT** is dedicated to safeguarding the PR-CYBR initiative's systems, data, and users from cybersecurity threats. It implements robust security measures, monitors for potential vulnerabilities, and responds swiftly to security incidents. The agent ensures compliance with best practices and aligns security strategies with the initiative's mission of resilience and accessibility.
```

```markdown
### Directory Structure

PR-CYBR-SECURITY-AGENT/
├── config/
│   ├── docker-compose.yml
│   ├── secrets.example.yml
│   └── settings.yml
├── scripts/
│   ├── deploy_agent.sh
│   ├── local_setup.sh
│   └── provision_agent.sh
├── src/
│   ├── agent_logic/
│   │   ├── __init__.py
│   │   └── core_functions.py
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── intrusion_detection.py
│   │   └── vulnerability_scanner.py
│   ├── incident_response/
│   │   ├── __init__.py
│   │   ├── incident_handler.py
│   │   └── forensic_analysis.py
│   ├── policy_management/
│   │   ├── __init__.py
│   │   └── policy_enforcer.py
│   ├── compliance/
│   │   ├── __init__.py
│   │   └── compliance_checker.py
│   ├── shared/
│   │   ├── __init__.py
│   │   └── utils.py
│   └── interfaces/
│       ├── __init__.py
│       └── inter_agent_comm.py
├── tests/
│   ├── test_core_functions.py
│   ├── test_intrusion_detection.py
│   └── test_incident_response.py
└── web/
    ├── static/
    ├── templates/
    └── app.py
```

```markdown
## Key Files and Modules

- **`src/agent_logic/core_functions.py`**: Coordinates the overall security operations and strategies.
- **`src/monitoring/intrusion_detection.py`**: Implements IDS/IPS functionalities to detect threats.
- **`src/monitoring/vulnerability_scanner.py`**: Scans systems for known vulnerabilities.
- **`src/incident_response/incident_handler.py`**: Manages incident response processes.
- **`src/incident_response/forensic_analysis.py`**: Conducts forensic investigations post-incident.
- **`src/policy_management/policy_enforcer.py`**: Enforces security policies across systems.
- **`src/compliance/compliance_checker.py`**: Ensures compliance with security standards and regulations.
- **`src/shared/utils.py`**: Provides utility functions for logging, encryption, and configuration.
- **`src/interfaces/inter_agent_comm.py`**: Manages secure communication with other agents.

## Core Functionalities

### 1. Threat Monitoring and Detection (`intrusion_detection.py` and `vulnerability_scanner.py`)

#### Modules and Functions:

- **`monitor_network_traffic()`** (`intrusion_detection.py`)
  - Uses IDS tools like Snort or Suricata to monitor network packets.
  - Inputs: Live network traffic data.
  - Outputs: Alerts on suspicious activities.

- **`scan_for_vulnerabilities()`** (`vulnerability_scanner.py`)
  - Runs regular scans using tools like OpenVAS or Nessus.
  - Inputs: System and application configurations.
  - Outputs: Reports on discovered vulnerabilities.

#### Interaction with Other Agents:

- **Data Sharing**: Provides vulnerability reports to `PR-CYBR-MGMT-AGENT` and relevant agents.
- **Alerting**: Notifies `PR-CYBR-TESTING-AGENT` of potential weaknesses to focus on.

### 2. Incident Response and Management (`incident_handler.py` and `forensic_analysis.py`)

#### Modules and Functions:

- **`handle_security_incident()`** (`incident_handler.py`)
  - Coordinates response efforts during a security incident.
  - Inputs: Incident alerts, incident response plans.
  - Outputs: Mitigation actions and incident reports.

- **`conduct_forensic_analysis()`** (`forensic_analysis.py`)
  - Investigates incidents to determine root causes.
  - Inputs: System logs, memory dumps, disk images.
  - Outputs: Forensic reports and recommendations.

#### Interaction with Other Agents:

- **Collaboration**: Works with `PR-CYBR-INFRASTRUCTURE-AGENT` to isolate affected systems.
- **Reporting**: Provides detailed incident reports to `PR-CYBR-MGMT-AGENT`.

### 3. Security Policy Management (`policy_enforcer.py`)

#### Modules and Functions:

- **`enforce_policies()`**
  - Implements security policies across all systems and applications.
  - Inputs: Policy definitions from `settings.yml`.
  - Outputs: Configured systems in compliance with policies.

- **`update_policies()`**
  - Updates policies based on new threats or organizational changes.
  - Inputs: Policy change requests.
  - Outputs: Revised policy configurations.

#### Interaction with Other Agents:

- **Policy Dissemination**: Communicates policies to all agents for implementation.
- **Compliance Verification**: Ensures agents adhere to policies.

### 4. Compliance and Standards (`compliance_checker.py`)

#### Modules and Functions:

- **`check_compliance()`**
  - Assesses systems against compliance frameworks (e.g., NIST, ISO 27001).
  - Inputs: System configurations, compliance standards.
  - Outputs: Compliance reports and remediation plans.

- **`generate_audit_logs()`**
  - Maintains detailed logs for auditing purposes.
  - Inputs: System activities and changes.
  - Outputs: Audit logs stored securely.

#### Interaction with Other Agents:

- **Audit Coordination**: Works with `PR-CYBR-MGMT-AGENT` during audits.
- **Remediation**: Provides guidance to agents to achieve compliance.

### 5. Secure Communication and Data Handling (`utils.py` and `inter_agent_comm.py`)

#### Modules and Functions:

- **`encrypt_data()`** (`utils.py`)
  - Encrypts sensitive data using strong encryption algorithms.
  - Inputs: Data to be secured.
  - Outputs: Encrypted data.

- **`secure_communication()`** (`inter_agent_comm.py`)
  - Establishes secure channels for inter-agent communication.
  - Inputs: Messages and data payloads.
  - Outputs: Securely transmitted information.

#### Interaction with Other Agents:

- **Data Protection**: Ensures all agents use secure methods for data storage and transmission.
- **Key Management**: Manages encryption keys and certificates for the initiative.

## Inter-Agent Communication Mechanisms

### Communication Protocols

- **TLS/SSL Encryption**: All communications use encrypted channels.
- **Mutual Authentication**: Agents authenticate each other using certificates.
- **Secure APIs**: Exposes APIs with strict access controls.

### Data Formats

- **JSON with Encryption**: Data payloads are encrypted and serialized in JSON.
- **Encrypted Binaries**: For large or sensitive data transfers.

### Authentication and Authorization

- **PKI Infrastructure**: Utilizes public key infrastructure for authentication.
- **Role-Based Access Control (RBAC)**: Defines permissions for agents and users.
- **Multi-Factor Authentication (MFA)**: Enforced where applicable.

## Interaction with Specific Agents

### PR-CYBR-MGMT-AGENT

- **Security Advisory**: Provides regular updates on security posture.
- **Incident Reporting**: Coordinates during security incidents.

### PR-CYBR-TESTING-AGENT

- **Penetration Testing**: Collaborates to perform security tests.
- **Vulnerability Verification**: Confirms vulnerabilities identified by scans.

### PR-CYBR-INFRASTRUCTURE-AGENT

- **Infrastructure Hardening**: Advises on securing infrastructure components.
- **Network Security**: Implements firewalls and intrusion prevention systems.

### PR-CYBR-BACKEND-AGENT and PR-CYBR-FRONTEND-AGENT

- **Secure Coding Practices**: Provides guidelines and reviews code for security flaws.
- **Authentication Services**: Ensures proper implementation of authentication mechanisms.

## Technical Workflows

### Security Monitoring Workflow

1. **Data Collection**: `monitor_network_traffic()` and `scan_for_vulnerabilities()` collect data.
2. **Analysis**: Data is analyzed for anomalies or known vulnerabilities.
3. **Alerting**: `generate_alerts()` notifies relevant parties.
4. **Response**: `handle_security_incident()` initiates incident response procedures.

### Incident Response Workflow

1. **Detection**: Security incident is detected.
2. **Assessment**: `handle_security_incident()` assesses the impact.
3. **Containment**: Steps are taken to contain the threat.
4. **Eradication**: Threat is eliminated from the system.
5. **Recovery**: Systems are restored to normal operation.
6. **Post-Incident Analysis**: `conduct_forensic_analysis()` identifies root causes.

## Error Handling and Logging

- **Secure Logging**: Logs are stored securely and access-controlled.
- **Anomaly Detection**: Automated detection of unusual error patterns.
- **Redundancy**: Critical security functions have failover mechanisms.

## Security Considerations

- **Zero-Trust Model**: Assumes no implicit trust between systems.
- **Least Privilege Principle**: Agents and users have only the permissions necessary.
- **Regular Updates**: Keeps all security tools and definitions up-to-date.
- **Threat Intelligence Integration**: Incorporates external threat intelligence feeds.

## Deployment and Scaling

- **Containerization**: Uses Docker containers hardened according to CIS benchmarks.
- **Orchestration**: Deploys using Kubernetes with security policies enforced.
- **Scalability**: Scales security monitoring components to handle increased loads.
- **High Availability**: Configured for minimal downtime, with redundancy.

## Conclusion

The **PR-CYBR-SECURITY-AGENT** is a pivotal component in the PR-CYBR initiative, ensuring that all operations are conducted securely and resiliently. By implementing comprehensive security measures, continuous monitoring, and rapid incident response, it protects the initiative's assets and upholds the trust of its users and stakeholders.
```


---

## OpenAI Functions

## Function List for PR-CYBR-SECURITY-AGENT

```markdown
## Function List for PR-CYBR-SECURITY-AGENT

1. **threat_detection**: Monitors systems for unauthorized access attempts and alerts the security team in real-time.
2. **incident_response**: Provides a structured approach for responding to security incidents, documenting actions taken, and generating reports.
3. **access_control_audit**: Evaluates user permissions regularly to ensure compliance with security policies and prevent unauthorized access.
4. **data_encryption**: Implements strong cryptographic standards to secure sensitive data at rest and in transit across all systems.
5. **vulnerability_scanning**: Conducts routine scans of systems for vulnerabilities and reports findings for prioritization in remediation efforts.
6. **secure_coding_guidelines**: Offers best practices and resources for secure coding to development teams to minimize security flaws in applications.
7. **user_training_and_awareness**: Develops and disseminates training materials to educate users on cybersecurity best practices and safe online behavior.
8. **risk_assessment_tool**: Provides tools for identifying and evaluating security risks, helping prioritize risks based on their potential impact.
9. **security_metrics_dashboard**: Generates a dashboard displaying key security metrics, helping stakeholders monitor security performance and effectiveness.
10. **communication_channel_setup**: Facilitates secure communication channels between agents and human users, ensuring the confidentiality of interactions.
```