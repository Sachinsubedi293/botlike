import time
import win32api
import win32con
import pywhatkit
import webbrowser
from vosk import Model, KaldiRecognizer
import openai
import pyttsx3
from AppOpener import open, close
import speech_recognition as sr
from google_speech import Speech
import os
import subprocess
engine = pyttsx3.init()

openai.api_key = "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"
url = "https://www.google.com/search?q="
messages = []
print("Your new assistant is ready!")
def clear():

    del_dir = r'C:\Users\nepal\AppData\Local\Temp'
    pObj = subprocess.Popen('del /S /Q /F %s\\*.*' % del_dir, shell=True, stdout = subprocess.PIPE, stderr= subprocess.PIPE)
    rTup = pObj.communicate()
    rCod = pObj.returncode
    if rCod == 0:
        print ('Success: Cleaned Windows Temp Folder')
        engine.say("Success: Cleaned Windows Temp Folder")
        engine.runAndWait()
    else:
        print ('Fail: Unable to Clean Windows Temp Folder')
        engine.say("Fail: Unable to Clean Windows Temp Folder")
        engine.runAndWait()

def volumeup():

    for x in range(10):
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0,
                             win32con.KEYEVENTF_KEYUP)

    # sleep is just to see the effect, it's not required here


def volumedown():
    for x in range(10):
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)

        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0,
                             win32con.KEYEVENTF_KEYUP)


def intent(app):
    if "." in app.lower():
        openurl = "www."+app.lower()
        webbrowser.open_new_tab(openurl)
    else:
        open(app.lower(), match_closest=True)


def closeintent(app):
    close(app.lower(), match_closest=True)


def recognize():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something")

        audio = r.listen(source)

        print("Recognizing Now .... ")

        # recognize speech using google

        try:
            while True:
                print("\nMe:" + r.recognize_google(audio))
                maintext = r.recognize_google(audio)
                print(maintext)
                sentence = maintext.split(" ")
                print(sentence)
                opentext = "open"
                closetext = "close"
                chatbot = "pokemon"
                search = "search"
                play = "play"
                volume = "volume"
                up = "up"
                down = "down"
                temp='clear'

                if opentext in sentence[0]:
                    intent(" ".join(sentence[1:len(sentence)]))
                    return "None"
                elif closetext in sentence[0]:
                    closeintent(" ".join(sentence[1:len(sentence)]))
                    return "None"
                elif chatbot in sentence[0].lower() and len(maintext) != 0:
                    return " ".join(sentence[1:len(sentence)])
                elif play in sentence[0]:
                    pywhatkit.playonyt(" ".join(sentence[1:len(sentence)]))
                    return "None"
                elif search in sentence[0]:
                    searchurl = url+" ".join(sentence[1:len(sentence)])
                    webbrowser.open_new_tab(searchurl)
                    return "None"
                elif volume in sentence[0] and up in sentence[1]:
                    volumeup()
                    return "None"
                elif volume in sentence[0] and down in sentence[1]:
                    volumedown()
                    return "None"
                elif temp in sentence[0]:
                    clear()
                    return "None"
                else:
                    return "None"

        except Exception as e:

            print("Error :  " + str(e))
            return "None"


while True:
    message = recognize()
    print(message)
    if message != "None":
        messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        print("\nBot:" + reply + "\n")
        # lang = "en"
        # speech = Speech(reply, lang)
        # sox_effects = ("speed", "1")
        # speech.play(sox_effects)
        engine.say(reply)
        engine.runAndWait()
