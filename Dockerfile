# =========================================================================
# BUILDER STAGE
# =========================================================================
FROM python:3.12-slim-trixie as builder

# 1. Install `uv` deterministically.
COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /bin/uv

# 2. Set up the working directory.
WORKDIR /usr/src/app

# 3. EXPLICITLY CREATE the virtual environment at a known path.
RUN python -m venv /opt/venv

# 4. ACTIVATE the environment for all subsequent commands.
ENV PATH="/opt/venv/bin:$PATH"

# 5. Copy dependency files.
COPY pyproject.toml uv.lock ./

# 6. Install dependencies.
RUN uv sync --no-cache-dir


# =========================================================================
# FINAL STAGE
# =========================================================================
FROM python:3.12-slim-trixie as final

# 1. Install essential runtime system dependencies.
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get -y upgrade --no-install-recommends \
 && apt-get -y install --no-install-recommends wget libsqlite3-0 build-essential libpq-dev  \
 && rm -rf /var/lib/apt/lists/*


# 2. Set the application's working directory.
WORKDIR /usr/src/app

# 3. Copy the ENTIRE pre-built virtual environment from the builder stage.
COPY --from=builder /usr/src/app/.venv /opt/venv

# 4. Copy the application source code.
COPY . .

# 5. Activate the virtual environment for the runtime.
ENV PATH="/opt/venv/bin:$PATH"

# 6. Define the command to run the application.
CMD ["python", "./server.py"]
