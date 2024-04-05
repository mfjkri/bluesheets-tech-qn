#!/bin/bash
prisma db push --schema=src/prisma/schema.prisma && prisma generate --schema=src/prisma/schema.prisma && uvicorn src.main:app --proxy-headers --host 0.0.0.0 --port 8888 --reload