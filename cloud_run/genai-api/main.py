from fastapi import FastAPI

from routers import gemini, hello_world


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(hello_world.router)
    app.include_router(gemini.router)
    return app


app = create_app()
