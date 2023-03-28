import RPi.GPIO as gp
import time

gp.setmode(gp.BOARD)
# gp.setup(11, gp.OUT)
# gp.setup(31, gp.OUT)
# gp.setup(35, gp.OUT)
# 
# gp.output(11, gp.HIGH)
# time.sleep(1)
# gp.output(31, gp.HIGH)
# time.sleep(1)
# gp.output(35, gp.HIGH)
# time.sleep(1)
# 
# gp.output(11, gp.LOW)
# time.sleep(1)
# gp.output(31, gp.LOW)
# time.sleep(1)
# gp.output(35, gp.LOW)
# time.sleep(1)


gp.setup(8, gp.IN)
count=0
while True:
    if gp.input(8)==1:
        print("Pin Released ", gp.input(8))
    else:
        print("Pin Pressed ", gp.input(8))
    
    