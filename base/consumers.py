from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .gpio_functions import *
from switches import devices
import json

class BaseConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.groups = None
        await self.accept()

    async def receive_json(self , content , *args , **kwargs):
        print(f"This is content : {content}")

        command = content.get("command")
        if command == "join_pi_group" : 
            groups =  await getGroupNames(self.user) 
            self.groups = groups
            for group_name in groups : 
                await self.joinGroup(group_name , self.channel_name)
            await self.sendMessage(
                {
                    "DATA_TYPE" : "GROUP_JOINED" ,
                    "data"      : "group_joined_successful" ,
                }
            )

        if command == "get_switch_list" :
            for device in devices :
                if devices[device][4] == "servo" :
                    devices[device][3] = gp.input(devices[device][5])
                    print(f"The servo device is : {devices[device]}")
                    print(f"The state checking is : {devices[device][5]}")
                    print(f"The state after checking is : {gp.input(devices[device][5])}")
                else :
                    devices[device][3] = gp.input(devices[device][1])
            message = {
                "DATA_TYPE"             : "SWITCH_BUTTON_LIST" , 
                "switch_list_data"      : devices ,
            }
            await self.sendMessage(message)

            

        if command == "change_switch_status" :
#             print("There is request to change switch status ")
            device_type = content.get("device_type")
#             print(f"The device type is  : {device_type}")
            button_number = content.get("button_number")
#             print(f"The button number is : {button_number}")
            state_change_value = content.get("state_change_value")
            if device_type == "relay" : 
                state_changed = await changePinStatus(button_number , state_change_value)
            if device_type == "servo" :
#                 print(f"The state_change_value for servo is : {state_change_value}")
                state_changed = await changeServoStatus(button_number , state_change_value)
#             print(f"The changed state value is  : {state_changed}")
            message = {
                    "type"                  : "sendMessage" ,
                    "DATA_TYPE"             : "BUTTON_STATE_CHANGE" ,
                    "state_change_value"    : state_change_value ,
                    "button_number"         : button_number ,
                }
            if state_changed :
                message["state_changed"] = True 
            else : 
                message["state_changed"] = False 
            for group in self.groups : 
                await self.groupMessageSend(group , message)

    async def joinGroup(self , group_name , channel_name) : 
        await self.channel_layer.group_add(
            group_name , 
            channel_name 
        )

    async def groupMessageSend(self , group_name , message):
        message["type"] = "sendMessage"
        await self.channel_layer.group_send(
            group_name , 
            message
        )

    async def sendMessage(self, message) :
        await self.send_json(
            message 
        )
        
            

    async def disconnect(self ,  close_code):
        await self.close(close_code)




@database_sync_to_async
def getGroupNames(user):
    return [ group.group_name for group in user.user_group.all() ]