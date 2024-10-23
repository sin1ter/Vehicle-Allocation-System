from fastapi import FastAPI
from routes.routes import router

app = FastAPI(
    title="Vehicle Allocation Management API",
    description="API for managing vehicle allocations",
    version="1.0.0",
)

app.include_router(router)