import speech_recognition as sr  
import pyttsx3
import bs4
import requests

try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

r = sr.Recognizer() 

engine = pyttsx3.init()

#generate a list of all audio cards/microphones
mic_name = 'MacBook Pro Microphone'

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
engine.setProperty('rate', 170)     # setting up new voice rate


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




#################### QUESTION SYNTAX  CHECK ###################
question_tags = ('what', 'how', 'who', 'where', 'when', 'is it')
question_follow = ('are', 'is', 'who', 'many', 'much', 'can', 'was', 'old')

def isQuestion(text1):
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

def deviceSwitch(code, text):
    success = 0
    categoryFound = False
    deviceFound = False
    for device in deviceList:
        if device in text:
            categoryFound = True
            for deviceName in deviceList[device]:
                if deviceName in text:
                    deviceFound = True
                    deviceList[device][deviceName]['status'] = code
                    success = 1
                    break
            if(categoryFound and not deviceFound):
                print(f"Which {device} do you mean?")
                engine.say("Which "+ device + "do you mean?")
                engine.runAndWait()
                for name in deviceList[device]:
                    engine.say(name)
                engine.runAndWait()
                #  RETRY DEVICE SEARCH
                for _ in range(3): 
                    r = sr.Recognizer() 
                    with sr.Microphone(device_index = device_id) as source: 
                                                                                       
                        print("Please specify device:")                                                                                   
                        audio = r.listen(source, phrase_time_limit=4)
                    try:
                        text = r.recognize_google(audio)
                        print(f"You said '{text}'")
                        for deviceName in deviceList[device]:
                            if deviceName in text:
                                deviceFound = True
                                deviceList[device][deviceName]['status'] = code
                                success = 1
                                break
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                    except sr.RequestError as e:
                        print("Could not request results; {0}".format(e))
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
        print("Sorry, I don't recognize that device.")
        engine.say("Sorry, I don't recognize that device.")
        engine.runAndWait()
       
            

def processText(text):
    if "turn on" in text:
        deviceSwitch(1, text)

    elif "turn off" in text:
        deviceSwitch(0, text)
    
    elif isQuestion(text):
        print("This is a question I have to search.")
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
    else: 
        print("unintelligible")
 


if __name__ == "__main__": 
    while("shut down" not in text): 
        r = sr.Recognizer() 
        with sr.Microphone(device_index = device_id) as source: 
            r.adjust_for_ambient_noise(source, duration = 3)  
            print("Say Hey John...")
            text = ''
            ##### wait for "hey John"... #####
            while('John' not in text):
                try: 
                    text = r.recognize_google(r.listen(source, phrase_time_limit=3) )
                except sr.UnknownValueError:
                    continue
            ##### START TAKING COMMAND... #####
            print("I am listening...")
           # print("Set minimum energy threshold to {}".format(r.energy_threshold))                                                                                                                                        
            audio = r.listen(source, phrase_time_limit=6) 
        try:
            text = r.recognize_google(audio)
            print(f"You said '{text}'")
            processText(text.lower())
        
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    print("shutting down...")
    engine.say("Shutting down")
    engine.runAndWait()

