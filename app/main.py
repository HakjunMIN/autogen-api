from .autogen_server import serve_autogen
from .data_model import Input
from fastapi import FastAPI
from starlette.responses import RedirectResponse

base = "/autogen/"
prefix = base + "api/v1"
openapi_url = prefix + "/openapi.json"
docs_url = prefix + "/docs"

app = FastAPI(
    title="Autogen FastAPI Backend",
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=None,
)

@app.get(path=base, include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url=docs_url)

@app.post(prefix + "/chat/completions")
async def route_query(model_input: Input):
    return serve_autogen(model_input)
