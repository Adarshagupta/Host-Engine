# Host-Engine

A Vercel-inspired platform for deploying web applications directly from Git repositories.

## Features

- **User Authentication**: Sign up and log in with email or GitHub
- **Project Management**: Connect GitHub repositories for deployment
- **Automatic Deployments**: Auto-deploy on git push
- **Custom Domains**: Connect your domains to your projects
- **Dashboard**: Monitor your deployments and projects

## Tech Stack

- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Deployment**: Docker, GitHub API
- **Task Queue**: Celery, Redis

## Project Structure

- `frontend/` - Next.js frontend application
- `backend/` - Python FastAPI backend
- `deployment/` - Deployment service for building and running applications

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Git

### Environment Setup

1. Setup environment variables:
   ```bash
   # For backend
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   
   # For frontend
   cp frontend/.env.example frontend/.env
   # Edit frontend/.env if needed
   ```

2. Database options:
   - **Local PostgreSQL**: Use the default configuration (postgres service in docker-compose.yml)
   - **External PostgreSQL (e.g., Neon, Azure)**: 
     1. Set `DATABASE_URL` in `backend/.env` to your connection string
     2. Remove or comment out the `postgres` service in `docker-compose.yml`
     3. Update the dependencies in the `backend` and `celery_worker` services

### Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/host-engine.git
   cd host-engine
   ```

2. Start the development environment:
   ```bash
   docker-compose up -d
   ```

3. Initialize the database:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Projects
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create a new project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Deployments
- `GET /api/v1/deployments` - List all deployments
- `POST /api/v1/deployments` - Create a new deployment
- `GET /api/v1/deployments/{id}` - Get deployment details
- `GET /api/v1/deployments/project/{project_id}` - Get deployments for a project

## License

This project is licensed under the MIT License - see the LICENSE file for details.
