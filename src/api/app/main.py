import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_profiler import PyInstrumentProfilerMiddleware

from .log_config import configure_azure_monitor_outer
from .routers import liveness, readiness, startup, test

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, debug=True)
app.add_middleware(
    PyInstrumentProfilerMiddleware,
    server_app=app,
    profiler_output_type="html",  # profiler_output_type="speedscope",
    html_file_name="profile.html",
    open_in_browser=True,
    is_print_each_request=True,  # prof_file_name="speedscope.json",
)
# register_middlewares(app)


# only set up OpenTelemetry logging if the OTEL environment variables are set
# if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT") is not None:
# setup_otel_logging(__name__, app)
configure_azure_monitor_outer()

app.include_router(test.router, prefix="/v1")
app.include_router(liveness.router, prefix="/v1")
app.include_router(readiness.router, prefix="/v1")
app.include_router(startup.router, prefix="/v1")
