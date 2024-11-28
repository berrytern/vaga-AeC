from src import app
from src.utils import settings

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.HTTP_PORT)