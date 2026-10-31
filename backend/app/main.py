from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import settings
from app.core.security_headers import SecurityHeadersMiddleware
from app.exceptions import register_exception_handlers
from app.logging import configure_logging
from app.middleware import RequestLoggingMiddleware

configure_logging()

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Enterprise backend API for SmartSpace AI.",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.backend_cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(_, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"success": False, "error": {"code": "rate_limited", "message": str(exc)}},
    )


register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": settings.app_name, "environment": settings.environment}

