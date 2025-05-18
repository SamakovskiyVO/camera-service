import psutil, pynvml, time
from utils import unix_ms

pynvml.nvmlInit()

def get_metrics():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=None)
    h = pynvml.nvmlDeviceGetHandleByIndex(0)
    util = pynvml.nvmlDeviceGetUtilizationRates(h)
    return {
        "timestamp": unix_ms(),
        "cpu_usage": cpu / 100.0,
        "gpu_usage": util.gpu / 100.0,
    }
