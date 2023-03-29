from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import RPi.GPIO as gp
import time 

channel_layer = get_channel_layer()

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
    print("Changing State")
    servo.ChangeDutyCycle(duty)
    gp.output(button_number, False)
    time.sleep(0.3)
    

def changePinStatus(button_number , state_change_value ):
    if state_change_value:
        gp.output(button_number, gp.HIGH)
        print("HIGH Signal Sent")
    else:
        gp.output(button_number, gp.LOW)
        print("Low Signal Sent")
        signal_sent = True
    message = {
        "type"                  : "sendMessage" , 
        "DATA_TYPE"             : "BUTTON_STATE_CHANGE" ,
        "state_change_value"    : state_change_value ,
        "button_number"         : button_number ,
        "state_changed"         : True , 
    }
    async_to_sync(channel_layer.group_send)(
        "NORS" ,
        message , 
    )
        
    return True

def changeServoPinStatus(button_number , state_change_value):
    try : 
        if state_change_value :
            print("Request for onn the servo")
            setAngle(button_number , 30)
        else :
            print("Reuqest for off the servo")
            setAngle(button_number , 60)
        for servo in servo_data :
            if servo_data[servo][1] == button_number :
                gp.setup(servo_data[servo][5] , gp.OUT)
                gp.output(servo_data[servo][5] , state_change_value)
        message = {
        "type"                  : "sendMessage" , 
        "DATA_TYPE"             : "BUTTON_STATE_CHANGE" ,
        "state_change_value"    : state_change_value ,
        "button_number"         : button_number ,
        "state_changed"         : True , 
        }
        async_to_sync(channel_layer.group_send)(
            "NORS" ,
            message ,
        )
        signal_sent = True
    except Exception as e:
        print(f"The exception is : {e}")
        signal_sent = False
    return signal_sent
