import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()

# Environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
# Define log files
APP_LOGGER_FILE = os.getenv("APP_LOGGER_FILE", "app.log")
# Define exceptions log file
EXCEPTIONS_LOGGER_FILE = os.getenv("EXCEPTIONS_LOGGER_FILE", "exceptions.log")

# Define the port for the HTTP server
HTTP_PORT = int(os.getenv("PORT_HTTP", "8000"))

# Define the issuer for the JWT
ISSUER = os.getenv("ISSUER", "berrytern")
# Define admin's username and password
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
# Define the password salt rounds
PASSWORD_SALT_ROUNDS = int(os.getenv("PASSWORD_SALT_ROUNDS", "12"))
# Define JWT secret
JWT_SECRET = os.getenv("JWT_SECRET")
# Define database URL
POSTGRES_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://admin:admin@localhost/aec?prepared_statement_cache_size=500",
)
