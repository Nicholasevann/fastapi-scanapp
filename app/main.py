from fastapi import FastAPI,Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints.api import api_router
from app.core.config import settings
from app.database import engine, Base
from starlette.middleware.base import BaseHTTPMiddleware
import json

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
class DefaultResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude OpenAPI and docs endpoints (with or without prefix)
        if any(
            request.url.path.endswith(path)
            for path in ["/openapi.json", "/docs", "/redoc"]
        ):
            return await call_next(request)
        response = await call_next(request)
        if response.headers.get("content-type", "").startswith("application/json"):
            body = [section async for section in response.body_iterator]
            raw_body = b"".join(body).decode()
            try:
                data = json.loads(raw_body)
            except Exception:
                data = raw_body

            if response.status_code >= 400:
                # Use detail as message if present, remove data
                message = data.get("detail") if isinstance(data, dict) and "detail" in data else "Error"
                wrapped = {
                    "statusCode": response.status_code,
                    "message": message,
                }
            else:
                wrapped = {
                    "statusCode": response.status_code,
                    "message": "Success",
                    "data": data
                }
            return JSONResponse(content=wrapped, status_code=response.status_code)
        return response

app.add_middleware(DefaultResponseMiddleware)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Template"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}