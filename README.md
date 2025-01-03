# AeC Backend Application

A FastAPI-based backend application developed as part of the application process for the Backend Developer (Pleno) position at AeC Brasil. The project implements a book management system with reader authentication and favorite book tracking.

## Features

- User Authentication and Authorization
  - Resource ownership validation
- Book Management (CRUD operations)
- Reader Profile Management
- Favorite Books System
- PostgreSQL Database Integration
- Automated Database Migrations with version control
- Redis-based response caching
- Async Operations
- HTTPS support
- Docker Containerization
- Application Monitoring and Observability
  - Real-time metrics collection
  - Performance tracking
  - Request/Response monitoring
- Automated Alert System
  - Email notifications for critical events
  - Customizable alert thresholds
  - Proactive system monitoring

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (Async)
- Alembic (Database Migration Tool)
  - Version-controlled schema changes
  - Automatic migration generation
  - Forward and rollback support
- PostgreSQL
- Redis
- Docker & Docker Compose
- Pydantic for data validation
- JWT Authentication
- Monitoring Stack
  - Prometheus for metrics collection
  - Grafana for visualization
  - AlertManager for notification management
  - Pre-configured monitoring dashboards

## Prerequisites

- Docker and Docker Compose installed
- Git for cloning the repository
- A text editor for configuration files

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/berrytern/vaga-AeC.git
   cd vaga-AeC

2. Environment Setup
    1. Setup backend service
        - Copy the example environment file:
            ```sh
            cp .env.docker .env
            ```
        - Update the `.env` file with your configurations.
    2. Setup monitoring with grafana[Optional]
        - Copy the example environment file:
            ```sh
            cp .env.config.grafana.example .env.config.grafana
            ```
    3. Setup email alerts [Optional]
        - Check the [EMAIL_ALERTS](./EMAIL_ALERTS.md) file

3. Build and Run with Docker:
    ```sh
    docker compose up -d --build
    ```
4. Verify the installation:
   - API Documentation: http://localhost:8000/docs
   - API health(grafana): http://localhost:3000/d/monitoring/service-monitoring

## Project Structure
```
.
├── src/
│   ├── application/         # Business logic and use cases
│   ├── infrastructure/      # Database and external services
│   ├── presenters/         # Controllers and routing
│   └── main/              # Application configuration
├── migrations/
│   ├── versions/           # Database migration files
│   ├── env.py             # Migration environment configuration
│   └── script.py.mako     # Migration script template
│   └── alembic.ini        # Alembic configuration file
```