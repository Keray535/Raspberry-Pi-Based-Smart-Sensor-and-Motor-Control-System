# system_stats.py
import psutil

def read_cpu_temp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            return float(f.read()) / 1000.0
    except:
        return None


def get_system_stats():
    cpu_temp = read_cpu_temp()
    cpu_pct  = psutil.cpu_percent(interval=None)
    ram_pct  = psutil.virtual_memory().percent
    return cpu_temp, cpu_pct, ram_pct