# Camera Frame-Quality Microservice

Микросервис принимает кадры, запускает модель качества
и публикует результат в ZCM-канале `FRAME_QUALITY_RESULT`.

* **Интерфейс** — ZCM (Zero Communication Middleware)  
* **Latency**    — \< 30 мс/кадр на Jetson AGX Xavier  
* **Контейнер**  — `docker build -t camera-service .`

## Быстрый запуск (локально)

git clone … camera-service
cd camera-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

правим config.yaml.example → config.yaml
python -m src.main --config config.yaml

## Быстрый запуск (Docker)

docker build -t camera-service docker/
docker run --gpus all \
  -v $(pwd)/config.yaml:/app/config.yaml \
  camera-service
  
## Каналы ZCM
Канал	Тип	Назначение
ipc://FRAME_QUALITY_RESULT	ZcmFrameQuality	Результаты инференса
ipc://CAMERA_DIAGNOSTIC_INFO	ZcmDiagInfo	CPU, GPU, latency

## Схемы находятся в zcm_types/*.zcm; генерируем C/Python-классы командой

zcm-gen -l python zcm_types/frame_quality.zcm
(для Python-рантайма ZCM должен быть установлен).

## Мини-CI

pytest -q
flake8 src/
