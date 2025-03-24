import uuid
import json
import chainlit as cl
from dotenv import load_dotenv
from openinference.instrumentation import using_session
from openinference.semconv.trace import SpanAttributes
from phoenix_config import TRACER
from llm_service import get_response
from tools import (
    fetch_db_info,
    auth_user
)

load_dotenv()

MESSAGE_HISTORY = []
session_id = str(uuid.uuid4())


@cl.on_chat_start
async def on_chat_start():
    cl.Message(content="Ask me anything!").send()


@cl.on_message
async def on_message(message: cl.Message):
    if not message.content:
        await cl.Message(content="Feel free to ask me anything!").send()

    with TRACER.start_as_current_span(name="agent", attributes={SpanAttributes.OPENINFERENCE_SPAN_KIND: "agent"}) as span:
        with using_session(session_id):
            span.add_event("チャットストリームを開始")
            span.set_attribute(SpanAttributes.INPUT_VALUE, message.content)
            
            MESSAGE_HISTORY.append({"role": "user", "content": message.content})
            response = get_response(MESSAGE_HISTORY)
            if response.choices[0].message.tool_calls:
                span.add_event("function calling の実施")
                tool_call = response.choices[0].message.tool_calls[0]
                args = json.loads(tool_call.function.arguments)
                tool_name = tool_call.function.name
                try:
                    if tool_name == "fetch_db_info":
                        result = fetch_db_info()
                    elif tool_name == "auth_user":
                        result = auth_user(args["username"], args["password"])
                    else:
                        raise ValueError(f"Unknown tool name: {tool_name}")
                except Exception as e:
                    raise e

                MESSAGE_HISTORY.append(response.choices[0].message)
                MESSAGE_HISTORY.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
                response = get_response(MESSAGE_HISTORY)
                MESSAGE_HISTORY.append(response.choices[0].message)

                response_content = response.choices[0].message.content
            else:
                response_content = response.choices[0].message.content
                MESSAGE_HISTORY.append({"role": "assistant", "content": response_content})

        span.set_attribute(SpanAttributes.OUTPUT_VALUE, response_content)
        await cl.Message(content=response_content).send()
