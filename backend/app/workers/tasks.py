from typing import Dict, Any, Optional
from celery import shared_task
import logging

from app.db.base import SessionLocal
from app.services.deployment import deployment_service
from app.api import crud

logger = logging.getLogger(__name__)


@shared_task
def deploy_project(deployment_id: str):
    """
    Task to handle the deployment process for a project
    """
    logger.info(f"Starting deployment: {deployment_id}")
    db = SessionLocal()
    
    try:
        # Get deployment
        deployment = crud.deployment.get_by_id(db=db, deployment_id=deployment_id)
        if not deployment:
            logger.error(f"Deployment not found: {deployment_id}")
            return
            
        # Update status to building
        crud.deployment.update_status(db=db, deployment_id=deployment_id, status="building")
        
        # Get project
        project = deployment.project
        
        # Clone repository
        repo_path, commit_hash, commit_message = deployment_service.clone_repository(
            repo_url=project.repository_url, 
            branch=project.branch
        )
        
        # Update deployment with commit info
        crud.deployment.update(
            db=db, 
            db_obj=deployment, 
            obj_in={
                "commit_hash": commit_hash,
                "commit_message": commit_message
            }
        )
        
        # Build project
        build_logs = deployment_service.build_project(
            repo_path=repo_path,
            build_command=project.build_command,
            output_dir=project.output_directory,
            env_vars=project.environment_variables
        )
        
        # Update with build logs
        crud.deployment.update(
            db=db, 
            db_obj=deployment, 
            obj_in={"build_logs": build_logs}
        )
        
        # Create deployment image
        image_tag = deployment_service.create_deployment_image(
            repo_path=repo_path,
            output_dir=project.output_directory,
            project_id=project.id,
            deployment_id=deployment.id
        )
        
        # Deploy the image
        deployment_url = deployment_service.deploy_image(
            image_tag=image_tag,
            deployment_id=deployment.id
        )
        
        # Update deployment with URL and status
        crud.deployment.update(
            db=db, 
            db_obj=deployment, 
            obj_in={
                "deployment_url": deployment_url,
                "status": "ready"
            }
        )
        
        # Clean up
        deployment_service.cleanup(repo_path)
        
        logger.info(f"Deployment completed: {deployment_id}")
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        
        # Update deployment with error
        if deployment:
            crud.deployment.update(
                db=db, 
                db_obj=deployment, 
                obj_in={
                    "status": "failed",
                    "error_message": str(e)
                }
            )
            
    finally:
        db.close() 