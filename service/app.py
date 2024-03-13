from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
import os
from fastapi.openapi.utils import get_openapi
from dependencies import get_logger

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            get_logger().critical(e, exc_info=True)
            return JSONResponse(
                status_code=500, 
                content={
                    'code': 500,
                    'data': None, 
                    'message': f'{e.__class__.__name__}: ' + str(e.args)
                }
            )

def lifespan(app: FastAPI):
    get_logger()
    yield

load_dotenv('.env')

dev_mode = os.environ.get('DEV', 'FALSE') == 'TRUE'

app = FastAPI(
    title="Service", 
    dependencies=[Depends(get_logger)],
    lifespan=lifespan,
    debug=dev_mode
)
app.add_middleware(ExceptionHandlerMiddleware)

def openapi_schema():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
       title="Service API",
       version="0.0",
       description="Microservice API",
       routes=app.routes,
   )
    app.openapi_schema = openapi_schema
    return openapi_schema

@app.get("/health", status_code=204, response_model=None)
async def health():
    pass

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={'data': None, 'code': exc.status_code, 'message': exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={'data': None, 'code': 400, 'message': exc.errors()})
