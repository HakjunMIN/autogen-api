from util.autogen_server import serve_autogen
from model.data_model import Input
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from workflow.autogen_workflow import AutogenWorkflow
from workflow.custom_workflow import CustomWorkflow

base = "/autogen/"
prefix = base + "api/v1/completions"
openapi_url = prefix + "/openapi.json"
docs_url = prefix + "/docs"

app = FastAPI(
    title="Autogen FastAPI Backend",
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=None,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path=base, include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url=docs_url)

@app.post(prefix + "/autogen-workflow")
async def route_autogen_workflow(model_input: Input):
    return serve_autogen(model_input, AutogenWorkflow)

@app.post(prefix + "/custom-workflow")
async def route_custom_workflow(model_input: Input):
    return serve_autogen(model_input, CustomWorkflow)

@app.get(prefix + "/health")
async def get_health():
    return {"status": "ok"}