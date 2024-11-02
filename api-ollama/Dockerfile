FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y wget

COPY ./presets/ ./root/.ollama/presets/

RUN chmod 777 -R ./root/.ollama/presets

RUN /root/.ollama/presets/init.sh