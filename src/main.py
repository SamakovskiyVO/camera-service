import argparse, yaml, cv2, zcm
from pathlib import Path
from collections import deque
from utils import unix_ms
from model import QualityModel
from diagnostics import get_metrics
from zcm_types import frame_quality as fq  # сгенерируется zcm-gen

def dominant(prob):
    idx = prob.argmax()
    names = ["good","rain","fog","snow","glare","dark","dirt"]
    return names[idx], idx != 0

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    return p.parse_args()

def main():
    args = parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text())

    z = zcm.ZCM("ipc")
    model = QualityModel(cfg["model_path"], cfg["device"])
    buf = deque(maxlen=cfg["buffer_size"])

    # подписка на кадры -------------------------------------------------
    def on_frame(channel, msg):
        frame = cv2.imdecode(msg.data, cv2.IMREAD_COLOR)
        probs = model.infer(frame)
        buf.append(probs)

        # majority окно
        if len(buf) == buf.maxlen:
            maj_idx = (sum(p.argmax() for p in buf) // len(buf))
        else:
            maj_idx = probs.argmax()

        dom, alert = dominant(probs)
        out = fq.ZcmFrameQuality()
        out.timestamp       = unix_ms()
        out.frame_id        = msg.frame_id
        out.quality_probs   = probs.tolist()
        out.alert_flag      = bool(alert)
        out.dominant_defect = dom
        z.publish(cfg["pub_channel"], out)

        # диагностика каждые 30 кадров
        if msg.frame_id % 30 == 0:
            d = get_metrics()
            diag = fq.ZcmDiagInfo()
            diag.timestamp  = d["timestamp"]
            diag.cpu_usage  = d["cpu_usage"]
            diag.gpu_usage  = d["gpu_usage"]
            diag.latency_ms = msg.latency_ms
            z.publish(cfg["diag_channel"], diag)

    z.subscribe(cfg["sub_channel"], on_frame)
    print("camera-service started")
    z.run()

if __name__ == "__main__":
    main()
