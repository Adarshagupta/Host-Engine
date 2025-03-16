from fastapi import APIRouter

from app.api.routes import auth, users, projects, deployments, domains
from app.api.endpoints import webhooks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(deployments.router, prefix="/deployments", tags=["deployments"])
api_router.include_router(domains.router, prefix="/domains", tags=["domains"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"]) 