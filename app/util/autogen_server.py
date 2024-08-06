import json
import traceback
import uuid
from queue import Queue
from threading import Thread

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from workflow.autogen_workflow import AutogenWorkflow
from model.data_model import Input, Output

def serve_autogen(inp: Input, autogenWorkflow: AutogenWorkflow = AutogenWorkflow):
    model_dump = inp.model_dump()
    model_messages = model_dump["messages"]
    workflow = autogenWorkflow()

    if inp.stream:
        queue = Queue()
        workflow.set_queue(queue)
        Thread(
            target=workflow.run,
            args=(
                model_messages[-1],
                inp.stream,
            ),
        ).start()
        return StreamingResponse(
            return_streaming_response(queue),
            media_type="text/event-stream",
        )
    else:
        chat_results = workflow.run(
            message=model_messages[-1],
            stream=inp.stream,
        )
        return return_non_streaming_response(chat_results)


def return_streaming_response(queue: Queue):
    while True:
        message = queue.get()
        if message == "[DONE]":
            yield "data: [DONE]\n\n"
            break
        chunk = Output(
            id=str(uuid.uuid4()),
            object="chat.completion.chunk",
            choices=[message]
        )
        yield f"data: {json.dumps(chunk.model_dump())}\n\n"
        queue.task_done()


def return_non_streaming_response(chat_results):
    try:
        if chat_results:
            return Output(
                id=str(chat_results.chat_id),
                choices=[
                    {"index": i, "message": msg, "finish_reason": "stop"}
                    for i, msg in enumerate(chat_results.chat_history)
                ],
            ).model_dump()
        else:
            return Output(
                id="None",
                choices=[
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "Sorry, I am unable to assist with that request at this time.",
                        },
                        "finish_reason": "stop"
                    }
                ],
            ).model_dump()

    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
