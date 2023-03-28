from channels.db import database_sync_to_async
import RPi.GPIO as gp
import time
from switches import devices

servo_data = {
    1 : [3 , 12 , "light" ,         gp.input(11) , "servo", 11] , 
    2 : [5 , 32 , "fan"   ,         gp.input(21) , "servo", 31] , 
    3 : [7 , 33 , "water_pump" ,    gp.input(7) , "servo", 35] ,
}
def setAngle(button_number , angle):
    """
    For settings servo angle 
    0deg : onn ,
    90deg : off ,  
    """
    gp.setup(button_number , gp.OUT)
    servo = gp.PWM(button_number , 50)
    
    servo.start(45)
    duty = angle / 18 + 2
    gp.output(button_number, True)
#     print("Changing State")
    servo.ChangeDutyCycle(duty)
    gp.output(button_number, False)
    time.sleep(0.3)
    


@database_sync_to_async
def changePinStatus(button_number , state_change_value):
#     print("The function was run and command was sent to change state !")
#     print(f"The button number is : {button_number} ")
#     print(f"The state change value : {state_change_value}")
    try :
#         print(f"The state change value is : {state_change_value}")
        if state_change_value:
            gp.output(button_number, gp.HIGH)
            print("HIGH Signal Sent")
        else:
            gp.output(button_number, gp.LOW)
            print("Low Signal Sent")   
        signal_sent = True
    except Exception as e:
        print(e)
        signal_sent = False
    return signal_sent



@database_sync_to_async
def changeServoStatus(button_number , state_change_value):
    try :
        if state_change_value :
            setAngle(button_number , 0)
        else :
            setAngle(button_number , 90)
        for servo in servo_data :
            if servo_data[servo][1] == button_number :
                gp.setup(servo_data[servo][5] , gp.OUT)
                gp.output(servo_data[servo][5] , state_change_value)
            
        signal_sent = True
        
    except :
        signal_sent = False
    return signal_sent