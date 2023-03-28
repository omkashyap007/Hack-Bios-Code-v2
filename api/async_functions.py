# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# import RPi.GPIO as gp
#  
# channel_layer = get_channel_layer()
# def changePinStatus(button_number , state_change_value ):
#     if state_change_value:
#         gp.output(button_number, gp.HIGH)
#         print("HIGH Signal Sent")
#     else:
#         gp.output(button_number, gp.LOW)
#         print("Low Signal Sent")
#         signal_sent = True
#     message = {
#         "type"                  : "sendMessage" , 
#         "DATA_TYPE"             : "BUTTON_STATE_CHANGE" ,
#         "state_change_value"    : state_change_value ,
#         "button_number"         : button_number ,
#         "state_changed"         : True , 
#     }
#     async_to_sync(channel_layer.group_send)(
#         "NORS" ,
#         message , 
#     )
#         
#     return True
# 