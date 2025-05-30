# sensors.py
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

class SensorReader:
    def __init__(self, dht_pin, trig_pin, echo_pin):
        self.dht = adafruit_dht.DHT11(dht_pin)
        self.trig = trig_pin
        self.echo = echo_pin
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def read_temperature_humidity(self):
        try:
            return self.dht.temperature, self.dht.humidity
        except RuntimeError as e:
            print(f"DHT error: {e}")
            return None, None

    def read_distance(self, timeout=0.05):
        try:
            GPIO.output(self.trig, False)
            time.sleep(0.05)
            GPIO.output(self.trig, True)
            time.sleep(1e-5)
            GPIO.output(self.trig, False)

            start = time.time()
            while GPIO.input(self.echo) == 0:
                if time.time() - start > timeout:
                    return None
            t0 = time.time()
            while GPIO.input(self.echo) == 1:
                if time.time() - t0 > timeout:
                    return None
            return (time.time() - t0) * 34300 / 2
        except Exception as e:
            print(f"HC-SR04 error: {e}")
            return None