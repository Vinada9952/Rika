import RPi.GPIO as GPIO
import time


class ServoMotor:

    def __init__(self, pin: int, start_position):
        self.pin = pin
        self.position = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        # PWM à 50Hz (standard servo)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

        self.moveServo(start_position)

    def moveServo(self, degree: float):

        # Limite de sécurité
        if degree < 0:
            degree = 0
        elif degree > 180:
            degree = 180

        self.position = degree

        # Conversion angle → duty cycle
        duty_cycle = 2.5 + (degree / 180.0) * 10

        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.3)

        # Stop léger signal pour éviter tremblement
        self.pwm.ChangeDutyCycle(0)

    def getPosition(self):
        return self.position

    def getPin(self):
        return self.pin

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()


# =====================
# TEST
# =====================

try:
    my_servo = ServoMotor(17, 90)

    while True:
        for i in range(180):
            my_servo.moveServo(i)
            print(i)

        for i in range(180):
            my_servo.moveServo(180 - i)
            print(180 - i)

except KeyboardInterrupt:
    print("Arrêt propre")
    my_servo.cleanup()