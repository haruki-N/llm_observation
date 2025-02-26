from openai import OpenAI
import os
from dotenv import load_dotenv
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

load_dotenv()

def setup_phoenix_project(project_name: str):
    tracer_provider = register(
        project_name=project_name,
        # gRPC endpoint for the Phoenix agent
        endpoint = "http://phoenix:4317"
    )
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    return tracer_provider

def main():
    _tracer_provider = setup_phoenix_project(project_name="phoenix-trials-from-docker")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "What is the capital of France?"}],
    )
    print(response)

if __name__ == "__main__":
    main()
