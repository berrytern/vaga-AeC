#!/bin/bash
set -e

# Executa as migrações
alembic upgrade head

# Inicia a aplicação
exec python ./server.py