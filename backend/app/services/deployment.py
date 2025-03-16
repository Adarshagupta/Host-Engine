import os
import uuid
import tempfile
import shutil
import subprocess
import docker
from typing import Optional, Dict, Any, List, Tuple
import git
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class DeploymentService:
    """Service for handling project deployments"""

    def __init__(self):
        try:
            # Try to connect using the Unix socket directly
            self.docker_client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Docker client: {str(e)}")
            self.docker_client = None
        
    def clone_repository(self, repo_url: str, branch: str = "main") -> Tuple[str, str]:
        """Clone a git repository and return the path and commit hash"""
        temp_dir = tempfile.mkdtemp()
        try:
            repo = git.Repo.clone_from(repo_url, temp_dir, branch=branch)
            commit_hash = repo.head.commit.hexsha
            commit_message = repo.head.commit.message
            return temp_dir, commit_hash, commit_message
        except Exception as e:
            shutil.rmtree(temp_dir)
            logger.error(f"Error cloning repository: {e}")
            raise
            
    def build_project(
        self, 
        repo_path: str, 
        build_command: Optional[str], 
        output_dir: str,
        env_vars: Dict[str, str] = None
    ) -> str:
        """Build the project and return the build output"""
        if not env_vars:
            env_vars = {}
            
        build_env = os.environ.copy()
        build_env.update(env_vars)
        
        try:
            output = ""
            
            if build_command:
                # Execute build command
                process = subprocess.Popen(
                    build_command,
                    shell=True,
                    cwd=repo_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=build_env,
                    text=True
                )
                
                for line in process.stdout:
                    output += line
                    
                process.wait()
                
                if process.returncode != 0:
                    raise Exception(f"Build failed with exit code {process.returncode}")
                    
            # Ensure output directory exists
            build_output_path = os.path.join(repo_path, output_dir)
            if not os.path.exists(build_output_path):
                os.makedirs(build_output_path)
                
            return output
            
        except Exception as e:
            logger.error(f"Error building project: {e}")
            raise
            
    def create_deployment_image(
        self, 
        repo_path: str, 
        output_dir: str,
        project_id: str,
        deployment_id: str
    ) -> str:
        """Create a docker image for the deployment"""
        try:
            # Create a simple Dockerfile for the static files
            dockerfile_content = """
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
            """
            
            # Write Dockerfile to the output directory
            build_output_path = os.path.join(repo_path, output_dir)
            with open(os.path.join(build_output_path, "Dockerfile"), "w") as f:
                f.write(dockerfile_content)
                
            # Build the Docker image
            image_tag = f"{settings.DOCKER_REGISTRY}/{project_id}:{deployment_id}"
            self.docker_client.images.build(
                path=build_output_path,
                tag=image_tag,
                rm=True
            )
            
            # Push the image to the registry if using external registry
            if settings.DOCKER_REGISTRY != "localhost:5000":
                self.docker_client.images.push(image_tag)
                
            return image_tag
                
        except Exception as e:
            logger.error(f"Error creating deployment image: {e}")
            raise
            
    def deploy_image(self, image_tag: str, deployment_id: str) -> str:
        """Deploy the image and return the deployment URL"""
        try:
            # Create a unique name for the container
            container_name = f"host-engine-{deployment_id[:8]}"
            
            # Run the container
            container = self.docker_client.containers.run(
                image_tag,
                name=container_name,
                detach=True,
                ports={"80/tcp": None},  # Auto-assign a port
                restart_policy={"Name": "always"}
            )
            
            # Get the assigned port
            container.reload()
            host_port = list(container.ports.get("80/tcp", []))[0]["HostPort"]
            
            # Construct the deployment URL
            deployment_url = f"http://{settings.POSTGRES_SERVER}:{host_port}"
            
            return deployment_url
            
        except Exception as e:
            logger.error(f"Error deploying image: {e}")
            raise
            
    def cleanup(self, repo_path: str):
        """Clean up temporary files"""
        try:
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
        except Exception as e:
            logger.error(f"Error cleaning up: {e}")


deployment_service = DeploymentService() 