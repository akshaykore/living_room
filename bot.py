# bot.py

# speechrecognition, pyaudio, brew install portaudio
import sys
sys.path.append("./")

import requests
import datetime
import dateutil.parser
import RPi.GPIO as GPIO 
import time
import json
import traceback
import pygame
from nlg import NLG
from speech import Speech
#from knowledge import Knowledge
#from vision import Vision


my_name = "Akshay"
launch_phrase = "Hey Cortana"
use_launch_phrase = False
#weather_api_token = "99e95a29cb1392b274cf27ea0399d6a5"
wit_ai_token = "Bearer BLZL5I25SBFTLXQBOVEQJVNUFX6F4J3T"
#youtube_api_token = "&key=AIzaSyAMOJ1NeL8h0XX5AV4bcG6AdIOFb1GMMOw"
debugger_enabled = True
camera = 0

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# init list with pin numbers

fan_gpio=2
light_gpio=3
lamp_gpio=17
charger_gpio=27
toaster_gpio=22
f=22 #TO BE USED FOR DIMMER LIGHT
g=10 #TO BE USED FOR DIMMER OF DEVICE
laptop_charger_gpio=9

pinList = [fan_gpio, light_gpio, lamp_gpio, charger_gpio, toaster_gpio, f, g, laptop_charger_gpio]

# loop through pins and set mode and state to 'low'

for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)
    print("                                 making everything an output")

class Bot(object):
    def __init__(self):
        self.nlg = NLG(user_name=my_name)
        self.speech = Speech(debugger_enabled=debugger_enabled) #(launch_phrase=launch_phrase, debugger_enabled=debugger_enabled)
        #self.knowledge = Knowledge(weather_api_token)
        #self.vision = Vision(camera=camera)

    def start(self):
        """
        Main loop. Waits for the launch phrase, then decides an action.
        :return:
        """
        while True:
            #requests.get("http://localhost:8080/clear")
            #if self.vision.recognize_face():
                #print ("Found face")
            if use_launch_phrase:
                recognizer, audio = self.speech.listen_for_audio()
                if self.speech.is_call_to_action(recognizer, audio):
                    self.__acknowledge_action()
                    self.decide_action()
            else:
                self.decide_action()

    def decide_action(self):
        """
        Recursively decides an action based on the intent.
        :return:
        """
        recognizer, audio = self.speech.listen_for_audio()

        # received audio data, now we'll recognize it using Google Speech Recognition
        speech = self.speech.google_speech_recognition(recognizer, audio)

        if speech is not None:
            try:
                r = requests.get('https://api.wit.ai/message?v=20160918&q=%s' % speech,
                                 headers={"Authorization": wit_ai_token})
                print (r.text)
                json_resp = json.loads(r.text)
                entities = None
                intent = None
                if 'entities' in json_resp and 'Intent' in json_resp['entities']:
                    entities = json_resp['entities']
                    intent = json_resp['entities']['Intent'][0]["value"]

                print (intent)
                if intent == 'greeting':
                    self.__text_action(self.nlg.greet())
                elif intent == 'joke':
                    self.__joke_action()
                elif intent == 'insult':
                    self.__insult_action()
                    return
                elif intent == 'appreciation':
                    self.__appreciation_action()
                    return

                elif intent == 'hello': #hello to AI
                    self.__hello_action()
               
                elif intent == 'music': #Playing Music
                    self.__music_action()
                    
                elif intent == 'stop playing': #Stop playing music
                    self.__stop_playing_action()

                elif intent == 'fan': #Start fan
                    self.__fan_on_action()
                elif intent == 'fan off': #Stop fan
                    self.__fan_off_action()

                elif intent == 'dim off': #Stop dimmer
                    self.__dim_off_action()
                    
                elif intent == 'dim low': #dimmer 25
                    self.__dim_low_action()
                    
                elif intent == 'dim high': #dimmer 75
                    self.__dim_high_action()
                    
                elif intent == 'dim full': #dimmer 100
                    self.__dim_full_action()

                elif intent == 'lights': #Switch on lights
                    self.__lights_on_action()
                    
                elif intent == 'lights off': #Switch off Lights
                    self.__lights_off_action()

                elif intent == 'good morning': #Good morning routine
                    self.__good_morning_action()

                elif intent == 'good night': #Good night routine
                    self.__good_night_action()

                elif intent == 'goodbye': #Goodbye routine
                    self.__goodbye_action()
                    
                elif intent == 'I am home': #i am home to AI
                    self.__iamhome_action()
                    
                elif intent == 'study time': #study time to AI
                    self.__study_action()
                
                elif intent == 'charge my phone': #charge my phone to AI
                    self.__phonecharge_action()
                
                elif intent == 'charge my laptop': #charge my laptop to AI
                    self.__laptopcharge_action()
          
                else: # No recognized intent
                    #self.__text_action("I'm sorry, I don't know about that yet.")
                    return

            except Exception as e:
                print ("Failed wit!")
                print(e)
                traceback.print_exc()
                self.__text_action("I'm sorry, I couldn't understand what you meant by that")
                return

            self.decide_action()

    def __joke_action(self):
        joke = self.nlg.joke()

        if joke is not None:
            self.__text_action(joke)
        else:
            self.__text_action("I couldn't find any jokes")

    def __appreciation_action(self):
        self.__text_action(self.nlg.appreciation())

    def __insult_action(self):
        self.__text_action(self.nlg.insult())

    def __text_action(self, text=None):
        if text is not None:
            requests.get("http://localhost:8080/statement?text=%s" % text)
            self.speech.synthesize_text(text)
            

    def __hello_action(self):
        print("Hello! I am kore!!!!!")
        GPIO.output(fan_gpio, GPIO.LOW)
        GPIO.output(light_gpio, GPIO.LOW)
        GPIO.output(lamp_gpio, GPIO.LOW)
        GPIO.output(charger_gpio, GPIO.LOW)
        GPIO.output(toaster_gpio, GPIO.LOW)
        GPIO.output(f, GPIO.LOW)
        GPIO.output(g, GPIO.LOW)
        GPIO.output(laptop_charger_gpio, GPIO.LOW)
        
        

    #FAN
    def __fan_on_action(self):
        print("Fan is on!")
        GPIO.output(fan_gpio, GPIO.LOW)
        

    def __fan_off_action(self):
        print("Fan is off!")
        GPIO.output(fan_gpio, GPIO.HIGH)


    #Lights
    def __lights_on_action(self):
        print("Lights on!")
        GPIO.output(light_gpio, GPIO.LOW)

    def __lights_off_action(self):
        print("Lights off!")
        GPIO.output(light_gpio, GPIO.HIGH)


    #Dimmer
    def __dim_off_action(self):
        print("Dimmer off!")

    def __dim_low_action(self):
        print("Dimmer at 25!")

    def __dim_high_action(self):
        print("Dimmer at 75!")

    def __dim_full_action(self):
        print("Dimmer full!")

        
    #Good morning
    def __good_morning_action(self):
        print("Good morning!")
        GPIO.output(fan_gpio, GPIO.LOW)     #Fan On
        GPIO.output(toaster_gpio, GPIO.LOW)    #Toaster On
        GPIO.output(light_gpio, GPIO.HIGH)  #lights off
        #dimmer to zero
        
    #Good night
    def __good_night_action(self):
        print("Good night!")
        GPIO.output(fan_gpio, GPIO.LOW)     #Fan On
        GPIO.output(light_gpio, GPIO.HIGH)  #everything off
        GPIO.output(lamp_gpio, GPIO.HIGH)
        GPIO.output(charger_gpio, GPIO.HIGH)
        GPIO.output(toaster_gpio, GPIO.HIGH)
        GPIO.output(f, GPIO.LOW)            #dimmer on to 5%
        GPIO.output(g, GPIO.HIGH)
        GPIO.output(laptop_charger_gpio, GPIO.HIGH)
       

    #Goodbye
    def __goodbye_action(self):
        print("Good bye!")
        GPIO.output(fan_gpio, GPIO.HIGH)    #everything off
        GPIO.output(light_gpio, GPIO.HIGH)
        GPIO.output(lamp_gpio, GPIO.HIGH)
        GPIO.output(charger_gpio, GPIO.HIGH)
        GPIO.output(toaster_gpio, GPIO.HIGH)
        GPIO.output(f, GPIO.HIGH)
        GPIO.output(g, GPIO.HIGH)
        GPIO.output(laptop_charger_gpio, GPIO.HIGH)
   
    #Studytime
    def __study_action(self):
        print("Good morning!")
        GPIO.output(lamp_gpio, GPIO.LOW) #lamp on
        GPIO.output(fan_gpio, GPIO.LOW)  #Fan on
        #Dimmer Low
        GPIO.output(laptop_charger_gpio, GPIO.LOW)  #laptop charger on
        pygame.mixer.init()
        pygame.mixer.music.load("thunder.mp3")                                                          #change file to some other good mp3
        pygame.mixer.music.play()                   #play soothing music to help concentration
        
    #I'm home
    def __iamhome_action(self):
        print("Welcome home!")
        GPIO.output(fan_gpio, GPIO.LOW)     #fan on
        GPIO.output(light_gpio, GPIO.LOW)   #lights on
        GPIO.output(f, GPIO.LOW) #Turn Dimmer on
        GPIO.output(g, GPIO.LOW)
        pygame.mixer.init()
        pygame.mixer.music.load("thunder.mp3")                                                          #change file to some highway to hell  mp3
        pygame.mixer.music.play()                   #play welcome music
    
    #Charge my phone
    def __phonecharge_action(self):
        print("Charging your Phone!")
        GPIO.output(charger_gpio, GPIO.LOW)
    
    #Charge my laptop
    def __laptopcharge_action(self):
        print("Charging your Phone!")
        GPIO.output(laptop_charger_gpio, GPIO.LOW)
        

    def __music_action(self):
        text = "playing your morning playlist"
        musicicon = "fa fa-play"
        name = "Thunder, by Imagine Dragons"
        text_obj = {"text_content":text, "musicicon": musicicon, "name": name}

        #self.speech.synthesize_text(text)
        #music
        pygame.mixer.init()
        pygame.mixer.music.load("thunder.mp3")
        pygame.mixer.music.play()
        


    def __stop_playing_action(self):
        pygame.mixer.music.stop()

if __name__ == "__main__":
    bot = Bot()
    bot.start()
