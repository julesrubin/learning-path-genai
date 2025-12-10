from fastapi import FastAPI

from routers import hello_world


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(hello_world.router)
    return app


app = create_app()
