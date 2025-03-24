import os
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

# Initialize tracer provider and tracer
TRACER_PROVIDER = register(
    project_name="phoenix-run-on-docker",
    endpoint=os.getenv("COLLECTOR_ENDPOINT"),
    set_global_tracer_provider=False
)

# Setup OpenAI instrumentation
OpenAIInstrumentor().instrument(tracer_provider=TRACER_PROVIDER)

# Get tracer instance
TRACER = TRACER_PROVIDER.get_tracer(__name__)