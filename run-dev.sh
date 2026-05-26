#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="${SCRIPT_DIR}/main/xiaozhi-server"
IMAGE="xiaozhi-base"
CONTAINER_NAME="xiaozhi-dev"

docker run --rm -it \
  --name "${CONTAINER_NAME}" \
  --security-opt seccomp=unconfined \
  -e TZ=Asia/Ho_Chi_Minh \
  -p 8000:8000 \
  -p 8003:8003 \
  -v "${SERVER_DIR}:/opt/xiaozhi-esp32-server" \
  "${IMAGE}" \
  python app.py
