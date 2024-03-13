from enum import IntEnum
import os
import logging, logging.config
from icecream import ic
import jwt
import requests
from httpx import AsyncClient
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.base import CertificatePublicKeyTypes
from commons.types import OperationResult
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
import time

logger : logging.Logger = None


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/health") == -1

def get_logger():
    global logger
    if logger is None:
        logger = logging.getLogger('service')
        # Filter out health checks
        logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
    return logger