from fastapi import FastAPI

from routers import gemini, hello_world, product_description, product_image, rag


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(hello_world.router)
    app.include_router(gemini.router)
    app.include_router(product_description.router)
    app.include_router(product_image.router)
    app.include_router(rag.router)
    return app


app = create_app()
