import uvicorn

from api import app
from config import config


def start_app():
    uvicorn.run("api:app", host=config.api_host, port=config.api_port, reload=True)


if __name__ == "__main__":
    start_app()
