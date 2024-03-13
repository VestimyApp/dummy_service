#!/bin/bash
DEV=TRUE python3 -m uvicorn service.app:app --host 0.0.0.0 --port 4600 --reload