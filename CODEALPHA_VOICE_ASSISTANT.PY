import speech_recognition as sr
import pyttsx3
import openai
from datetime import datetime
import webbrowser

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
openai.api_key = 'your-openai-api-key'

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, there seems to be a problem with the service.")
            return ""

def process_command(command):
    if "hello" in command:
        speak("Hello Raghav ! How can I assist you today?")
    elif "time" in command:
        current_time = datetime.now().strftime('%I:%M %p')
        speak(f"The time is {current_time}")
    elif "open" in command and "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "send a mail" in command :
        speak("Sure Raghav!")
        webbrowser.open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox?compose=new")
    elif "exit" in command or "take a nap" in command:
        speak("If any need arises remember, your assistent is here raghav")
        return True  
    else:
        response = get_nlp_response(command)
        speak(response)

def get_nlp_response(command):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=command,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "Sorry, I can't answer that right now."

speak("Initializing voice assistan...")
while True:
    user_command = listen()
    if process_command(user_command): 
        break 