import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()


HTTP_PORT = int(os.getenv("PORT_HTTP", "8000"))

# Define jwt secret
JWT_SECRET = os.getenv("JWT_SECRET")
POSTGRE_URL = os.getenv(
    "POSTGRE_URL",
    "postgresql+asyncpg://admin:admin@localhost/aec?prepared_statement_cache_size=500",
)
