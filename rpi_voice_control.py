import switches as sw
import requests
import os
import speech_recognition as sr
recog = sr.Recognizer()
devices = sw.devices


# text = "turn on switch 1"
one = ["1", "one", "on"]
two = ["2", "two", "to"]
three = ["3", "three"]
four = ["4", "four", "for"]
five = ["5", "five"]


def number_map(n):
    if n in one:
        return 1
    if n in two:
        return 2
    if n in three:
        return 3
    if n in four:
        return 4
    if n in five:
        return 5
    return None


def split_commands(text):
    text = text.lower()
    text = text.split(" ")
    print(text)
    switch = None
    change_state = None
    if 'switch' in text:
        print("switch is in text")
        switch = text[text.index('switch')+1]
        print(switch)
        try:
            switch = int(switch)
        except:
            switch = number_map(switch)
        finally:
            switch = devices[switch][1]
        print(switch)

        if any(state in text for state in ["on", "onn"]):
            change_state = 1
        elif any(state in text for state in ["off", "of"]):
            change_state = 0
        print(switch,'  ', change_state)
        
    response = createRequest(switch, change_state)
    print(dict(response))


def createRequest(button_number, state_change_value):
    if button_number in sw.PWM:
        api_url = 'http://localhost:8080/api/change-servo-device-state/'
    else:
        api_url = 'http://localhost:8080/api/change-device-state/'
    data = {"button_number" : button_number , "state_change_value": state_change_value}
    headers = {"Authorization": f"Bearer {os.environ.get('BIOS_TOKEN')}"}
    response = requests.post(
        url = api_url ,
        data = data ,
        headers = headers )

    print("Request Recieved : change state of {} to {}".format(
        button_number, state_change_value))
    print(dict(response.json()))
    return response


while True:	
    with sr.Microphone() as mic:
        recog.adjust_for_ambient_noise(mic)
        print("Software is listening ... ")
        audio = recog.listen(mic)
        print("Voice captured ...")

    try:
        text = recog.recognize_google(audio)
        print(text)
        split_commands(text)
    except Exception as e:
        print("Error occured:" + str(e))
