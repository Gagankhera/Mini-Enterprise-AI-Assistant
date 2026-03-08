"""FastAPI application entry point."""

# IMPORTANT: Load .env file FIRST, before any LangChain imports
# This ensures LangSmith environment variables are available for tracing

from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app import __version__
from app.api.routes import chat, documents, health, integration, agent
from app.config import get_settings
from app.logger import get_logger, setup_logging

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging(settings.log_level)
    logger = get_logger(__name__)
    logger.info(f"Starting {settings.app_name} v{__version__}")
    logger.info(f"Log level: {settings.log_level}")

    yield

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
## "Mini Enterprise AI Assistant"

A Context-aware document chatbot (RAG) question-answering system built with:
- **FastAPI** for the API layer
- **LangChain** for RAG orchestration
- **Faiss** for vector storage
- **OpenAI** for embeddings and LLM

### Features
- Upload PDF, TXT, and CSV documents
- Ask questions and get AI-powered answers
- View source documents for transparency
    """,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include routers
app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(integration.router)
app.include_router(agent.router)


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger = get_logger(__name__)
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
        },
    )


if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )


'''
@app.post("/agent/analyze")
def analyze():

    return analyze_security_logs()


@app.get("/integration/github-summary")
def github():

    return github_summary()
    '''