from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.container import Container
from src.presentation.routers import task_router

# Initialize dependency injection container
container = Container()

# Create FastAPI application
app = FastAPI(
    title="Task API",
    description="A RESTful API for managing tasks.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router.router)


@app.on_event("startup")
def startup_event():
    container.wire(modules=[task_router])


@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Task API",
        "version": "0.1.0"
    }


@app.on_event("shutdown")
def shutdown_event():
    container.unwire()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
