import time
import logging
import random
import string
import sys

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from mangum import Mangum

from . import auth, const, router_users, router_groups

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

stage = const.STAGE
root_path = f"/{stage}" if stage else ""
app = FastAPI(title="WF Google Workspace API", root_path=root_path)

token_auth_scheme = HTTPBearer()


# DO NOT ATTEMPT TO CAPTURE REQUEST BODY HERE, IT WILL CAUSE THE APP TO FREEZE
@app.middleware("http")
async def log_request_timing(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    request.state.idem = idem

    logger.info(f"rid={idem} start request_path={request.url.path}")

    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} complete completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


async def log_request_details(request: Request):
    headers = '\r\n\t'.join('{}: {}'.format(k, v) for k, v in request.headers.items())
    body = await request.body()
    logger.info("""rid={rid} details
    {method} {url}

    HEADERS:
    {headers}

    BODY:
    {body}
    """.format(rid=request.state.idem, method=request.method, url=request.url, headers=headers, body=body.decode("utf-8")))


app.include_router(router_users.router, dependencies=[Depends(log_request_details)])
app.include_router(router_groups.router, dependencies=[Depends(log_request_details)])


@app.get("/")
async def hola_mundo():
    return JSONResponse(content={"message": '¡Hola, mundo!'})


@app.exception_handler(404)
def resource_not_found(request, ex):
    return JSONResponse(status_code=404, content={"error": ex.detail if hasattr(ex, 'detail') else "Not Found"})


@app.exception_handler(auth.AuthError)
def handle_auth_error(request, ex):
    logger.exception(ex)
    return JSONResponse(status_code=ex.status_code, content=ex.error)


@app.exception_handler(Exception)
async def handle_general_exception(request, ex):
    logger.exception(ex)
    return JSONResponse(status_code=500, content="Unexpected server error")


handler = Mangum(app)
