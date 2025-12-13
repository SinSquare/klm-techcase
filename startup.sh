#!/bin/bash

alembic upgrade head
fastapi run klm_techcase/main.py --port 80
