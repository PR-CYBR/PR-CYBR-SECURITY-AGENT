# Agent Documentation

This document provides information about the agent's functionality, setup, and usage.

## Overview

(Provide an overview of the agent here.)

## Setup Instructions

(Provide setup instructions here.)

## Usage

(Provide usage instructions here.)

## Dry-Run Testing Guidance

To validate Notion synchronisation changes before merging to the mainline branch, run a dry-run workflow in GitHub Actions using the preconfigured `workflow_dispatch` trigger:

1. Push your feature branch to the remote repository (avoid pushing directly to `main` in accordance with the PR-CYBR branching model).
2. Navigate to the repository's **Actions** tab and select the Notion sync workflow.
3. Choose **Run workflow** and target your staging branch; supply a JSON payload representative of the records you intend to sync. Example payload:

   ```json
   {
     "entities": [
       {
         "id": "sample-1",
         "title": "Dry Run Entity",
         "description": "Validation before production push",
         "status": "Draft",
         "tags": ["staging", "validation"]
       }
     ],
     "mappings": {
       "sample-1": "new"
     }
   }
   ```

4. Confirm the workflow executes against the staging environment and review the structured log output for entity-level status indicators (`created`, `updated`, `missing_mapping`, `not_found`, and `failed`).
5. Iterate on the branch as needed until the dry-run completes without errors, then open a pull request targeting the staging branch for further review.
