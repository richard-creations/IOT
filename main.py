import speech_recognition as sr  
import pyttsx3
import pprint
engine = pyttsx3.init()

#generate a list of all audio cards/microphones
mic_name = "MacBook Pro Microphone"

mic_list = sr.Microphone.list_microphone_names()
print(mic_list)

#select the device if based the mic name

for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic_name:
        device_id = i

print(f"Using mic: {mic_list[device_id]}")
# get audio from the microphone 


##### SPEECH VOICE SET-UP ########
""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 160)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female
                                                                      
engine.say("Alfred is starting up.")
engine.runAndWait()

##### END  SPEECH SET-UP ########

##################### DEVICE LISTS ##################
text = ''
deviceList = {}
deviceList['light'] = {'bedroom':{'status': 0 }, 'living room':{'status': 0 }, 'outside': {'status': 0 }} 
deviceList['speaker'] = {'bedroom':{'status': 0 }, 'google home':{'status': 0 }, 'jbl':{'status': 0 }, 'amazon echo':{'status': 0 }}
#################### END DEVICE LISTS ##################




#################### QUESTION SYNTAX ###################
question_tags = ('what', 'how', 'who', 'where', 'when', 'is it')
modifiers = ('many', 'much', 'can' )
question_follow = ('are', 'is', 'who'  )

def isQuestion():
    return 0

##################### END QUESTION TEXT ##############

def deviceSwitch(code, text):
    success = 0
    for device in deviceList:
        if device in text:
            print(device) 
            for deviceName in deviceList[device]:
                if deviceName in text:
                    print(deviceName)
                    deviceList[device][deviceName]['status'] = code
                    success = 1
                    break
            break

    if success == 1:      
        if code == 0:
            print(f'{deviceName} {device} is now turned off')
            engine.say(deviceName + " "+ device +" is now turned off")
            engine.runAndWait()
        if code == 1:
            print(f'{deviceName} {device} is now turned on')
            engine.say(deviceName + " "+ device +" is now turned on")
            engine.runAndWait()
        print(deviceList)
    else:
        print("Sorry, device not recognized")
        engine.say("Sorry, device not recognized")
        engine.runAndWait()
       
            

def processText(text):
    if "turn on" in text:
        deviceSwitch(1, text)

    if "turn off" in text:
        deviceSwitch(0, text)
    
    if "what is" in text or "how" in text or "when" in text:
        return 0

if __name__ == "__main__":
    while("shut down" not in text):
        r = sr.Recognizer()  
      
        with sr.Microphone(device_index = device_id) as source: 
            r.adjust_for_ambient_noise(source)                                                                      
            print("Speak:")                                                                                   
            audio = r.listen(source) 
        try:
            text = r.recognize_google(audio)
            print(f"You said '{text}'")
            processText(text.lower())
        
        except sr.UnknownValueError:
            print("Could not understand audio")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    print("shutting down...")
    engine.say("Shutting down")
    engine.runAndWait()

