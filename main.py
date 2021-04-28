from MicManager import MicManager
from VoiceAssistant import VoiceAssistant
from QueryManager import QueryManager
from DeviceManager import DeviceManager


voiceEngine = VoiceAssistant().getEngine()
deviceManager = DeviceManager()
queryManager = QueryManager()
micManager = MicManager()
     
text = ''


def processText(text):
    if "turn on" in text:
        deviceManager.deviceSwitch(1, text)

    elif "turn off" in text:
        deviceManager.deviceSwitch(0, text)
    
    elif queryManager.isQuestion(text):
        queryManager.getResults(text)
    else: 
        print("unintelligible")
 


if __name__ == "__main__": 
    while("shut down" not in text): 
        r = micManager.getRecognizer() 
        with micManager.getSR().Microphone(device_index = micManager.getDeviceID()) as source: 
            r.adjust_for_ambient_noise(source, duration = 3)  
            print("Say Hey John...")
            text = ''

            ##### wait for "hey John"... #####
            while('John' not in text):
                try: 
                    text = r.recognize_google(r.listen(source, phrase_time_limit=3) )
                except micManager.getSR().UnknownValueError:
                    continue
            ##### START TAKING COMMAND... #####

            print("I am listening...")                                                                                                                                      
            audio = r.listen(source, phrase_time_limit=6) 
        try:
            text = r.recognize_google(audio)
            print(f"You said '{text}'")
            processText(text.lower())
        
        except micManager.getSR().UnknownValueError:
            continue
        except micManager.getSR().RequestError as e:
            print("Could not request results; {0}".format(e))
    print("shutting down...")
    voiceEngine.say("Shutting down")
    voiceEngine.runAndWait()

