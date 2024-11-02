#!/bin/bash

CONTAINER_NAME="pds-ollama"
SCRIPT_PATH="./root/.ollama/presets/model_runner.sh"

docker exec -it "$CONTAINER_NAME" bash "$SCRIPT_PATH"