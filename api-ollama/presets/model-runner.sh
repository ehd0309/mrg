#!/bin/bash

MODEL_LIST=('qwen/qwen-7b-fp16' 'qwen/qwen-14b-fp16' 'yanolja/eeve-10.8b-fp16')

chmod +x -R /root/.ollama/presets/

for model in "${MODEL_LIST[@]}"
do
  if [ "$(ollama list $model | wc -l)" -gt 1 ]; then
    echo "Model $model already exists, skipping..."
  else
    echo "Model $model not found, running /root/.ollama/presets/$model.sh"
    "/root/.ollama/presets/$model.sh"
  fi
done

echo "All models checked."