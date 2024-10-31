import os
import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.log_config import configure_azure_monitor_outer
from app.routers import analyze, liveness, readiness, startup
from app.dependencies import setup_dependencies

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_dependencies()
    yield

app = FastAPI(lifespan=lifespan, debug=True)

# only set up OpenTelemetry logging if the OTEL environment variables are set
# if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT") is not None:
# setup_otel_logging(__name__, app)
if os.environ.get("APPLICATION_INSIGHTS_CONNECTION_STRING") != "":
    configure_azure_monitor_outer()

app.include_router(analyze.router, prefix="/v1")
app.include_router(liveness.router, prefix="/v1")
app.include_router(readiness.router, prefix="/v1")
app.include_router(startup.router, prefix="/v1")
