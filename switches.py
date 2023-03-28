import RPi.GPIO as gp
gp.setmode(gp.BOARD)
SWITCH=[None, 3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21]
RELAY=[None, 40, 38, 37, 36, 35, 33, 32, 31, 29, 26, 24, 23, 22]
PWM=[None,12,32,33,35]
# device ={devicenumber : [commandpin, executerpin, device name, current state]}

print(list(zip(SWITCH, RELAY))[1:])
for switch, relay in list(zip(SWITCH, RELAY))[1:]:
    gp.setup(switch, gp.IN)
    gp.setup(relay, gp.OUT)

devices = {
    1 : [3 , 12 , "light" ,         gp.input(11) , "servo", 11] , 
    2 : [5 , 32 , "fan"   ,         gp.input(21) , "servo", 31] , 
    3 : [7 , 33 , "water_pump" ,    gp.input(7) , "servo", 35] ,
    4 : [8 , 38 , "fan" ,           gp.input(38) , "relay", None ] ,
    5 : [10, 40 , "fan" ,           gp.input(40) , "relay", None ] ,
}
# for device in devices:
#     gp.setup

for switch in devices:
    print(f"{switch} : {devices[switch][1]}")
"""
switch id : gpioPin : pinNumber
switch device : (fan , light ....)
initial_state of devices : onn / off

servo switch : led
3 : 11
5 :31
7 : 35

"""