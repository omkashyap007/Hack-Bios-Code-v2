import time
import requests
import switches as sw
import RPi.GPIO as gp
import os
token = os.environ.get("BIOS_TOKEN")
print(token)
gp.setmode(gp.BOARD)
# device ={devicenumber : [commandpin, executerpin, device name, current state, executer type]}

print("FIRING UP RASP.PY")

devices = sw.devices
for device in devices.values():
    print(device)
    gp.setup(device[0], gp.IN)  # index 0 is command pin or the button.
    gp.setup(device[1], gp.OUT) # index 1 is executer pin or the relay
    if device[4]=="servo":
        gp.setup(device[5], gp.OUT)

last_state=[None]
for i in devices:
    last_state.append(gp.input(devices[i][0]))
print(last_state)

def toggleRelay(relay, is_toggle_button=False, toggle_status=0):
    """It will simply toggle the relay on or off """
    if is_toggle_button:
        if toggle_status==0:
            relay_state=1
        else:
            relay_state=0
    else:
        relay_state=gp.input(relay)
#     gp.output(relay, int(not relay_state))
    print("off" if relay_state==1 else "on")
    print(f"The value of relay is : {relay}")
    print(f"The value of change state is : {int(not relay_state)}")
    response = requests.post('http://localhost:8080/api/change-device-state/' ,
        data = {"button_number" : int(relay) , "state_change_value": int(not relay_state)} ,
        headers = {"Authorization": f"Bearer {token}" })
    print(response)
#     print(dict(response))
    
def toggleServo(device):
    
#     def setAngle(button_number , angle):
    """
    For settings servo angle 
    0deg : onn ,
    90deg : off ,  
    """
    button_number=device[1]
    led_pin=device[5]
    state = gp.input(led_pin)
    gp.output(led_pin, int(not state))
    response = requests.post(
            url = "http://localhost:8080/api/change-servo-device-state/" ,
            headers = {"Authorization" : f"Bearer {token}"} ,
            data = {"button_number" : button_number , "state_change_value" : int(not state) } , 
        )
    print(dict(response.json()))

    # set angle to 90 to turn if off as its state is 1 and vice versa
#     angle = 90 if state==1 else 0
#     
#     servo = gp.PWM(button_number , 50)
#     servo.start(45)
#     duty = angle / 18 + 2
#     gp.output(button_number, True)
    
# #     print("Changing State")
#     servo.ChangeDutyCycle(duty)
#     gp.output(button_number, False)
    time.sleep(0.5)
    

print("-"*10 + "Ready to Work" + '-'*10)

print(gp.input(devices[1][1]), devices[1][3])




while True :
    # check if current state of relay != last state as :
        # chck if the input button is pressed
            # if pressed then toggle
        # change last stae to current
    
    i=1		#device id
    if gp.input(devices[i][0]) != last_state[i]:
        print("waiting for button to be released")
        if gp.input(devices[i][0]) == 1:
            toggleServo(devices[i])
        last_state[i] = abs(1-last_state[i])
    
    i=2
    if gp.input(devices[i][0]) != last_state[i]:
        print("waiting for button to be released")
        if gp.input(devices[i][0]) == 1:
            toggleServo(devices[i])
        last_state[i] = abs(1-last_state[i])
    
    i=3
    if gp.input(devices[i][0]) != last_state[i]:
        print("waiting for button to be released")
        if gp.input(devices[i][0]) == 1:
            toggleServo(devices[i])
        last_state[i] = abs(1-last_state[i])
        
    i=4
#     if gp.input(devices[i][0]) == 0:
#         if gp.input(devices[i][0]) != last_state[i]:
#             print("Toggle Switch Is Active") 
#             toggleRelay(devices[i][1], True,0)
#         last_state[i] = abs(1-last_state[i])
        
    i=5
    if gp.input(devices[i][0]) != last_state[i]:
        print("waiting for button to be released")
        if gp.input(devices[i][0]) == 1:
            toggleRelay(devices[i][1])
        last_state[i] = abs(1-last_state[i])

