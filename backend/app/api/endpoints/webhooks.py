from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
import json
import hmac
import hashlib

from app.api import deps
from app.api.crud import project, deployment
from app.core.config import settings

router = APIRouter()

def verify_github_signature(signature: str, payload: bytes, secret: str) -> bool:
    """Verify that the webhook request is from GitHub."""
    if not signature:
        return False
    
    signature_parts = signature.split('=')
    if len(signature_parts) != 2:
        return False
    
    algorithm, signature_hash = signature_parts
    
    if algorithm != 'sha1':
        return False
    
    # Compute the HMAC
    hmac_obj = hmac.new(secret.encode(), payload, hashlib.sha1)
    expected_signature = hmac_obj.hexdigest()
    
    return hmac.compare_digest(signature_hash, expected_signature)

def process_deployment(
    project_id: str,
    commit_hash: str,
    commit_message: str,
    db: Session
) -> None:
    """Process a deployment in the background."""
    # Create a new deployment
    new_deployment = deployment.create_deployment(
        db=db,
        project_id=project_id,
        commit_hash=commit_hash,
        commit_message=commit_message
    )

@router.post("/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db)
):
    """Handle GitHub webhook events to trigger automated deployments."""
    # Get the signature from the headers
    signature = request.headers.get('X-Hub-Signature')
    
    # Read the request body
    payload = await request.body()
    
    # Parse the payload
    event_data = json.loads(payload)
    
    # Get the event type
    event_type = request.headers.get('X-GitHub-Event')
    
    # Only process push events
    if event_type != 'push':
        return {"status": "ignored", "reason": "Event type not supported"}
    
    # Get the branch that was pushed to
    ref = event_data.get('ref')
    if not ref:
        return {"status": "error", "reason": "No ref found in payload"}
    
    # Extract the branch name (e.g., from "refs/heads/main" to "main")
    branch = ref.replace('refs/heads/', '')
    
    # Get the repository information
    repository = event_data.get('repository', {})
    repo_url = repository.get('clone_url')
    
    if not repo_url:
        return {"status": "error", "reason": "No repository URL found in payload"}
    
    # Get the latest commit information
    commits = event_data.get('commits', [])
    if not commits:
        return {"status": "error", "reason": "No commits found in payload"}
    
    latest_commit = commits[0]
    commit_hash = latest_commit.get('id')
    commit_message = latest_commit.get('message')
    
    # Find projects that match this repository URL and branch
    projects = project.get_projects_by_repo_and_branch(
        db=db,
        repository_url=repo_url,
        branch=branch
    )
    
    if not projects:
        return {"status": "ignored", "reason": "No matching projects found"}
    
    # Trigger a deployment for each matching project
    for proj in projects:
        # Verify the webhook signature if a webhook secret is set for this project
        if proj.webhook_secret:
            if not verify_github_signature(signature, payload, proj.webhook_secret):
                continue  # Skip this project if signature verification fails
                
        # Schedule the deployment in the background
        background_tasks.add_task(
            process_deployment,
            project_id=proj.id,
            commit_hash=commit_hash,
            commit_message=commit_message,
            db=db
        )
    
    return {"status": "success", "message": "Deployment(s) triggered"}

@router.post("/gitlab")
async def gitlab_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db)
):
    """Handle GitLab webhook events to trigger automated deployments."""
    # Read the request body
    payload = await request.body()
    
    # Parse the payload
    event_data = json.loads(payload)
    
    # Get the event type
    event_type = request.headers.get('X-Gitlab-Event')
    
    # Only process push events
    if 'Push Hook' not in event_type:
        return {"status": "ignored", "reason": "Event type not supported"}
    
    # Get the branch that was pushed to
    ref = event_data.get('ref')
    if not ref:
        return {"status": "error", "reason": "No ref found in payload"}
    
    # Extract the branch name (e.g., from "refs/heads/main" to "main")
    branch = ref.replace('refs/heads/', '')
    
    # Get the repository information
    repo_url = event_data.get('project', {}).get('git_http_url')
    
    if not repo_url:
        return {"status": "error", "reason": "No repository URL found in payload"}
    
    # Get the latest commit information
    commits = event_data.get('commits', [])
    if not commits:
        return {"status": "error", "reason": "No commits found in payload"}
    
    latest_commit = commits[0]
    commit_hash = latest_commit.get('id')
    commit_message = latest_commit.get('message')
    
    # Find projects that match this repository URL and branch
    projects = project.get_projects_by_repo_and_branch(
        db=db,
        repository_url=repo_url,
        branch=branch
    )
    
    if not projects:
        return {"status": "ignored", "reason": "No matching projects found"}
    
    # Trigger a deployment for each matching project
    for proj in projects:
        # Schedule the deployment in the background
        background_tasks.add_task(
            process_deployment,
            project_id=proj.id,
            commit_hash=commit_hash,
            commit_message=commit_message,
            db=db
        )
    
    return {"status": "success", "message": "Deployment(s) triggered"} 