# LLM observability with Phoenix

Imprementation of [Phoenix](https://phoenix.arize.com/) in Docker containers using [uv](https://astral.sh/uv/)
- you can trace & evaluate LLM calls with Phoenix

# deploy
docker compose up --build
Two services will be deployed.
- llm-server: Chainlit application. You can access it with `http://localhost:8000`
- phoenix: Phoenix server. You can access it with `http://localhost:6006`
