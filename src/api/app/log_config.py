from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.config import get_settings


def setup_otel_logging(module_name, app):
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer(module_name)

    otlp_exporter = OTLPSpanExporter()
    # we don't want to export every single trace by itself but rather batch them
    span_processor = BatchSpanProcessor(otlp_exporter)
    otlp_tracer = trace.get_tracer_provider().add_span_processor(span_processor)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=otlp_tracer)


def configure_azure_monitor_outer():
    configure_azure_monitor(
        connection_string=get_settings().application_insights_connection_string,
        enable_live_metrics=True,
    )
