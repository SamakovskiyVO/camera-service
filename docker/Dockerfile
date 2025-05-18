FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip \
    && pip3 install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY zcm_types/ zcm_types/
COPY config.yaml.example /app/config.yaml
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "src.main", "--config", "config.yaml"]
