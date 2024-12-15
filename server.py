from src import http_app, https_app
from src.utils import settings
from multiprocessing import Process


if __name__ == "__main__":
    import uvicorn

    p1 = Process(
        target=lambda: uvicorn.run(
            http_app,
            host="0.0.0.0",
            port=settings.HTTP_PORT,
        ),
        args=(),
    )
    p2 = Process(
        target=lambda: uvicorn.run(
            https_app,
            host="0.0.0.0",
            port=settings.HTTPS_PORT,
            ssl_certfile=settings.SSL_CERT_PATH,
            ssl_keyfile=settings.SSL_KEY_PATH,
        ),
        args=(),
    )
    p1.start()
    p2.start()
    p2.join()
