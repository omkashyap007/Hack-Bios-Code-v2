import time
import requests
import switches as sw
import RPi.GPIO as gp
import os
token = os.environ.get("BIOS_TOKEN")
print(token)
gp.setmode(gp.BOARD)
# device ={devicenumber : [commandpin, executerpin, device name, current 

devices = sw.devices
for device in devices.values():
    print(device)
    gp.setup(device[0], gp.IN)  # index 0 is command pin or the button.
    gp.setup(device[1], gp.OUT) # index 1 is executer pin or the relay
    

def toggleRelay(relay):
    """It will simply toggle the relay on or off """
    relay_state=gp.input(relay)
#     gp.output(relay, int(not relay_state))
    print("off" if relay_state==1 else "on")
    print(f"The value of relay is : {relay}")
    print(f"The value of change state is : {int(not relay_state)}")
    response = requests.post('http://localhost:8080/api/change-device-state/' ,
        data = {"button_number" : int(relay) , "state_change_value": int(not relay_state)} ,
        headers = {"Authorization": f"Bearer {token}" })
    print(response)
    
print("-"*10 + "Ready to Work" + '-'*10)

print(gp.input(devices[1][1]), devices[1][3])

last_state=[None]
for i in devices:
    last_state.append(gp.input(devices[i][0]))
print(last_state)

try:
    while True :
        # check if current state of relay != last state as :
            # chck if the input button is pressed
                # if pressed then toggle
            # change last stae to current
            
        i=1		#deivice id
        if gp.input(devices[i][0]) != last_state[i]:
            print("waiting for button to be released")
            if gp.input(devices[i][0]) == 1:
                toggleRelay(devices[i][1])
            last_state[i] = abs(1-last_state[i])
        
        i=2
        if gp.input(devices[i][0]) != last_state[i]:
            print("waiting for button to be released")
            if gp.input(devices[i][0]) == 1:
                toggleRelay(devices[i][1])
            last_state[i] = abs(1-last_state[i])
        i=3
        if gp.input(devices[i][0]) != last_state[i]:
            print("waiting for button to be released")
            if gp.input(devices[i][0]) == 1:
                toggleRelay(devices[i][1])
            last_state[i] = abs(1-last_state[i])
        
#         i=4
#         if gp.input(devices[i][0]) != last_state[i]:
#             print("waiting for button to be released")
#             if gp.input(devices[i][0]) == 1:
#                 toggleRelay(devices[i][1])
#             last_state[i] = abs(1-last_state[i])
#         
    
finally:
    gp.cleanup()
    print("CleanUp Complete")
