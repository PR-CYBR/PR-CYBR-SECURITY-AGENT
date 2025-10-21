# AgentKit for PR-CYBR-SECURITY-AGENT  

This document explains how to extend the AgentKit for the Security agent.  

## Adding Tasks  
- Edit `agentkit/config.yaml` and add new tasks under the `tasks` section.  
- Define the `tool`, `command`, and expected `output`.  

## Triggers  
- Use manual triggers (e.g., `/scan`) for on-demand scans.  
- Use scheduled triggers with cron syntax for periodic security checks.  

## Codex integration  
If Codex is unavailable, the fallback linter will run locally and log warnings. 
