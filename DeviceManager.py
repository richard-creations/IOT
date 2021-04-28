from VoiceAssistant import VoiceAssistant
from MicManager import MicManager


voiceEngine = VoiceAssistant().getEngine()

##### MIC SET-UP ########                                                                      
micManager = MicManager()
r = micManager.r
sr = micManager.getSR()
##### END  SPEECH SET-UP ########


##################### DEVICE LISTS ##################
text = ''
deviceList = {}
deviceList['light'] = {'bedroom':{'status': 0 }, 'living room':{'status': 0 }, 'outside': {'status': 0 }} 
deviceList['speaker'] = {'bedroom':{'status': 0 }, 'google home':{'status': 0 }, 'jbl':{'status': 0 }, 'amazon echo':{'status': 0 }}
#################### END DEVICE LISTS ##################



class DeviceManager:
    def __init__(self):
        self.hello = 0

    def deviceSwitch(self, code, text):
        success = 0
        categoryFound = False
        deviceFound = False
        for category in deviceList:
            if category in text:
                categoryFound = True
                for deviceName in deviceList[category]:
                    if deviceName in text:
                        deviceFound = True
                        deviceList[category][deviceName]['status'] = code
                        success = False
                        break
                if(categoryFound and not deviceFound):
                    print(f"Which {category} do you mean?")
                    voiceEngine.say("Which "+ category + "do you mean?")
                    voiceEngine.runAndWait()
                    for name in deviceList[category]:
                        voiceEngine.say(name)
                    voiceEngine.runAndWait()
                    #  RETRY DEVICE SEARCH
                    for _ in range(3): 
                        r = micManager.r
                        with sr.Microphone(device_index = micManager.getDeviceID()) as source: 
                                                                                        
                            print("Please specify category:")                                                                                   
                            audio = r.listen(source, phrase_time_limit=4)
                        try:
                            text = r.recognize_google(audio)
                            print(f"You said '{text}'")
                            for deviceName in deviceList[category]:
                                if deviceName in text:
                                    deviceFound = True
                                    deviceList[category][deviceName]['status'] = code
                                    success = True
                                    break
                        except sr.UnknownValueError:
                            print("Could not understand audio")
                        except sr.RequestError as e:
                            print("Could not request results; {0}".format(e))
                break
        #SUCCESS MESSAGE#
        if success == True:      
            if code == 0:
                print(f'{deviceName} {category} is now turned off')
                voiceEngine.say(deviceName + " "+ category +" is now turned off")
                voiceEngine.runAndWait()
            elif code == 1:
                print(f'{deviceName} {category} is now turned on')
                voiceEngine.say(deviceName + " "+ category +" is now turned on")
                voiceEngine.runAndWait()
                
            print(deviceList)
        else:
            print("Sorry, I don't recognize that category.")
            voiceEngine.say("Sorry, I don't recognize that category.")
            voiceEngine.runAndWait()
       