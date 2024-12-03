# AeC Backend Application

A FastAPI-based backend application developed as part of the application process for the Backend Developer (Pleno) position at AeC Brasil. The project implements a book management system with reader authentication and favorite book tracking.

## Features

- User Authentication and Authorization
- Book Management (CRUD operations)
- Reader Profile Management
- Favorite Books System
- PostgreSQL Database Integration
- Async Operations
- Docker Containerization

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Docker & Docker Compose
- Pydantic for data validation
- JWT Authentication

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
    - Copy the example environment file:
        ```sh
        cp .env.example .env
        ```
    - Update the `.env` file with your configurations:
3. Build and Run with Docker:
    ```sh
    docker compose up -d --build
    ```
4. Verify the installation:
   - API Documentation: http://localhost:8000/docs

## Project Structure
```
.
├── src/
│   ├── application/         # Business logic and use cases
│   ├── infrastructure/      # Database and external services
│   ├── presenters/         # Controllers and routing
│   └── main/              # Application configuration
```