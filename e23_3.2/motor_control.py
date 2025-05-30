# motor_control.py
import RPi.GPIO as GPIO

class MotorController:
    def __init__(self, in1, in2, ena, pwm_freq=1000):
        self.in1 = in1
        self.in2 = in2
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(ena, GPIO.OUT)
        self.pwm = GPIO.PWM(ena, pwm_freq)
        self.pwm.start(0)
        self.running = False
        self.stop_counter = 0

    def control(self, dist, temp, dist_thresh, temp_thresh, tolerance):
        condition = (dist is not None and dist < dist_thresh) and \
                    (temp is not None and temp > temp_thresh)
        if condition:
            if not self.running:
                GPIO.output(self.in1, GPIO.HIGH)
                GPIO.output(self.in2, GPIO.LOW)
                self.pwm.ChangeDutyCycle(80)
                print("Motor: ÇALIŞIYOR")
                self.running = True
            self.stop_counter = 0
        else:
            if self.running:
                self.stop_counter += 1
                print(f"Motor durma sayacı: {self.stop_counter}/{tolerance}")
                if self.stop_counter >= tolerance:
                    self.pwm.ChangeDutyCycle(0)
                    print("Motor: DURDU")
                    self.running = False
                    self.stop_counter = 0
            else:
                self.stop_counter = 0