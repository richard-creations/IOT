import pyttsx3


class VoiceAssistant:

    def __init__(self):
        self.engine = pyttsx3.init()
        ##### SPEECH VOICE SET-UP ########
        """ RATE"""
        self.rate = self.engine.getProperty('rate')   # getting details of current speaking rate
        self.engine.setProperty('rate', 170)     # setting up new voice rate


        """VOLUME"""
        self.volume = self.engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
        self.engine.setProperty('volume',1.0)               # setting up volume level  between 0 and 1

        """VOICE"""
        self.voices = self.engine.getProperty('voices')       #getting details of current voice
        #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
        self.engine.setProperty('voice', self.voices[0].id)   #changing index, changes voices. 1 for female
                                                                            
        #engine.say("Alfred is starting up.")
        self.engine.runAndWait()
        ##### END  SPEECH SET-UP ########

    def getEngine(self):
        return self.engine
       

    