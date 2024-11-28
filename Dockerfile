FROM python:3.11.2-slim-buster

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Configure Poetry
RUN poetry config virtualenvs.create false

# Set up working directory
WORKDIR /usr/src/app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Clean up build dependencies
RUN apt-get purge -y build-essential curl && apt-get autoremove -y

# Copy application code
COPY . .

EXPOSE 8000

CMD ["python", "./server.py"]