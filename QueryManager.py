from MicManager import MicManager
from VoiceAssistant import VoiceAssistant
from DeviceManager import DeviceManager
from VoiceAssistant import VoiceAssistant
from MicManager import MicManager
import speech_recognition as sr  
import bs4
import requests

try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

micManager = MicManager()

r = micManager.getRecognizer() 

engine = VoiceAssistant().getEngine()

#################### QUESTION SYNTAX  CHECK ###################
question_tags = ('what', 'how', 'who', 'where', 'when', 'is it')
question_follow = ('are', 'is', 'who', 'many', 'much', 'can', 'was', 'old')

class QueryManager():

    def isQuestion(self, text1):
        text = text1.split()
        for tag in question_tags: #O(n)
            try:
                index = text.index(tag) #O(1)
                if text[index +1] in question_follow: #O(n)
                    return True
            except:
                continue
        return False
    ##################### END QUESTION TEXT ##############


    def getResults(self, text):
        print("I have to look that up...")
        url = 'https://google.com/search?q=' + text
        
        # Fetch the URL data using requests.get(url),
        # store it in a variable, request_result.
        request_result=requests.get( url )
        
        # Creating soup from the fetched request
        soup = bs4.BeautifulSoup(request_result.text,
                                "html.parser")
        
        # soup.find.all( h3 ) to grab 
        # all major headings of our search result,
        heading_object=soup.find_all( 'h3' )
        
        # Iterate through the object 
        # and print it as a string.
        print(heading_object[0].getText())
        engine.say(heading_object[0].getText())
        engine.runAndWait()
        print("------")
