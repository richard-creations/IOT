
import speech_recognition as sr 


class MicManager:
    def __init__(self):
        self.r = sr.Recognizer() 
        #generate a list of all audio cards/microphones
        self.mic_name = 'MacBook Pro Microphone'

        self.mic_list = sr.Microphone.list_microphone_names()

        #select the device if based the mic name

        for i, microphone_name in enumerate(self.mic_list):
            if microphone_name == self.mic_name:
                self.device_id = i

    def getMicName(self):
        return self.mic_name
    
    def getSR(self):
        return sr

    def getDeviceID(self):
        return self.device_id

    def getRecognizer(self):
        return self.r