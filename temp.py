import time
import RPi.GPIO as gp
gp.setmode(gp.BOARD)
#12 32 33
servo_pin=12
gp.setup(servo_pin, gp.OUT)

servo=gp.PWM(servo_pin, 50)

servo.start(45)

def setAngle(angle):
    duty = angle / 18 + 2
    gp.output(servo_pin, True)
    print("Changing State")
    servo.ChangeDutyCycle(duty)
    gp.output(servo_pin, False)
#     time.sleep(1)
#     print("Going Back To Normal State")
#     gp.output(servo_pin, True)
#     servo.ChangeDutyCycle(90)
#     gp.output(servo_pin, False)

setAngle(45)