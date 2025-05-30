# main.py
import time
import RPi.GPIO as GPIO
import board
from sensors import SensorReader
from system_stats import get_system_stats
from utils import MovingAverage
from motor_control import MotorController

# --- Parametreler ---
DIST_SIZE      = 1        # Hareketli ortalama pencere boyutu
TEMP_SIZE      = 1        # Hareketli ortalama pencere boyutu
STOP_TOLERANCE = 3        # Koşul sağlanmazsa durdurma toleransı
BASE_DELAY     = 3        # Döngü gecikmesi (saniye)
DIST_THRESH    = 30       # cm, motor çalışması için maksimum mesafe
TEMP_THRESH    = 23       # °C, motor çalışması için minimum sıcaklık

# --- GPIO Mode ---
GPIO.setmode(GPIO.BCM)

# --- Örnek Pin Tanımları ---
dht_pin  = board.D17
trig_pin = 23
echo_pin = 24
in1_pin  = 27
in2_pin  = 22
ena_pin  = 18

# --- Nesne Oluşturma ---
sensor   = SensorReader(dht_pin, trig_pin, echo_pin)
stats    = get_system_stats  # fonksiyon referansı

dist_flt = MovingAverage(DIST_SIZE)
temp_flt = MovingAverage(TEMP_SIZE)
motor    = MotorController(in1_pin, in2_pin, ena_pin)

try:
    while True:
        ts = time.strftime('%Y-%m-%d %H:%M:%S')

        # Sistem Ölçümleri
        cpu_temp, cpu_pct, ram_pct = stats()

        # Sensör Ölçümleri
        temp, hum = sensor.read_temperature_humidity()
        dist = sensor.read_distance()

        # Filtreleme
        dist_flt.add(dist)
        temp_flt.add(temp)
        f_dist = dist_flt.average()
        f_temp = temp_flt.average()

        # Çıktı
        print(f"[{ts}] CPU: {cpu_temp or '----'}°C, CPU%: {cpu_pct:.1f}, RAM%: {ram_pct:.1f}")
        print(f"[{ts}] Sıcaklık: {temp or '----'}°C (filt: {f_temp or '----'}), Nem: {hum or '----'}%")
        # Mesafe için iki ondalık basamak
        dist_str = f"{dist:.2f}" if dist is not None else "----"
        f_dist_str = f"{f_dist:.2f}" if f_dist is not None else "----"
        print(f"[{ts}] Mesafe: {dist_str} cm (filt: {f_dist_str})")

        # Motor Kontrol (uzaklık <30 cm AND sıcaklık >23°C)
        motor.control(f_dist, f_temp, DIST_THRESH, TEMP_THRESH, STOP_TOLERANCE)

        print('-'*50)
        time.sleep(BASE_DELAY)

  
except KeyboardInterrupt:
    pass

finally:
	GPIO.cleanup()
	dht.exit()
