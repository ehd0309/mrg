FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openssh-client \
    build-essential \
    git


WORKDIR /app

FROM base AS jupyter-runner
COPY . .

RUN pip install -r requirements.txt
RUN pip install jupyter jupyterlab

# COPY jupyter_notebook_config.py /root/.jupyter/
ENV JUPYTER_TOKEN="1234"

EXPOSE 8888
ENV PORT=8888
ENV HF_HOME=/usr/.hf-cache

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]


FROM base AS flask-runner
COPY . .

RUN pip install -r requirements.txt
RUN pip install flask flask-cors gunicorn

EXPOSE 5000
ENV PORT=5000
ENV HF_HOME=/usr/.hf-cache

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "3", "--timeout", "7200", "app:app"]