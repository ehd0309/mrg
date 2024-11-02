wget -O /root/.ollama/presets/qwen/qwen-7b-fp16.gguf https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-f16.gguf

ollama create qwen/qwen-7b-fp16 -f /root/.ollama/presets/qwen/qwen-7b-fp16