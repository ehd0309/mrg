wget -O /root/.ollama/presets/qwen/qwen-14b-fp16.gguf https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/main/Qwen2.5-14B-Instruct-f16.gguf

ollama create qwen/qwen-14b-fp16 -f /root/.ollama/presets/qwen/qwen-14b-fp16