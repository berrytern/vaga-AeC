FROM python:3.11.2-slim-buster

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry and add to PATH
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

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

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Run the migrations and start the server
ENTRYPOINT ["/entrypoint.sh"]
