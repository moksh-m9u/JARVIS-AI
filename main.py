import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
from AppOpener import open as app_open
from AppOpener import close
import wikipedia
import google.generativeai as genai
import os
from google.generativeai import types
import requests
from dotenv import dotenv_values
env_vars=dotenv_values(".env")
GEMINIAPI=env_vars.get("GEMINIAPI")
# Voice output
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 170)
engine.setProperty('voice', voices[0].id)
engine.runAndWait()
# Function for Jarvis to speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
genai.configure(api_key=GEMINIAPI)
# Obtain audio from the microphone
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        content = r.recognize_google(audio, language='en-in')
        print("You said: " + content)
    except Exception as e:
        content = "0"
        print("Please try again...")
    return content
#image generation and download code
def download_image(image_url, filename="image.jpg"):
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Check if request was successful
        # Write the content to a file
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'Download Completed: {filename}')
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
def main_process():
    while True:
        request = command().lower()

        if "hello" in request:
            speak("Welcome, how can I help you?")

        elif "play music" in request:
            speak("Playing music")
            song = random.randint(1, 5)
            if song == 1:
                webbrowser.open("https://www.youtube.com/watch?v=cWMxCE2HTag")
            elif song == 2:
                webbrowser.open("https://www.youtube.com/watch?v=LK7-_dgAVQE")
            elif song == 3:
                webbrowser.open("https://www.youtube.com/watch?v=LYEqeUr-158")
            elif song == 4:
                webbrowser.open("https://www.youtube.com/watch?v=II2EO3Nw4m0")
            elif song == 5:
                webbrowser.open("https://www.youtube.com/watch?v=YR12Z8f1Dh8")

        elif "say time" in request:
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + str(now_time))

        elif "say date" in request:
            now_date = datetime.datetime.now().strftime("%d:%m")
            speak("Today's date is " + str(now_date))

        elif "new task" in request:
            task = request.replace("new task", " ")
            task = task.strip()
            if task != "":
                speak("Adding task: " + task)
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")

        elif "speak task" in request:
            with open("todo.txt", "r") as file:
                speak("Today we have to: " + file.read())

        elif "show task" in request:
            with open("todo.txt", "r") as file:
                tasks = file.read()
            speak("your task are shown in notifications")
            notification.notify(
                title="Today's Work",
                message=tasks
            )
        elif "open youtube"in request:
            webbrowser.open("www.youtube.com")
            speak("opening youtube")
        elif "open etawah"in request:
            webbrowser.open("ettiva.com")
            speak("openning ettiva")
        elif "open" in request:
            # Extract apps to open
            apps = request.replace("open", "").strip()
            apps=apps.replace(" ", ",")
            if apps:
                speak("Opening " + apps)
                app_open(apps,match_closest=True)  # Opens multiple apps separated by commas
            else:
                speak("Please specify what to open.")
        elif "close" in request:
            request=request.replace("close","")
            request= request.replace(" ",",")
            close(request)
        elif "search google" in request:
            request=request.replace("jarvis","")
            request=request.replace("search google","")
            request=request.replace("about","")
            webbrowser.open("https://www.google.com/search?q="+request)
        elif "wikipedia"in request:
            request=request.replace("search wikipedia","")
            request=request.replace("jarvis","")
            print ("searching about"+request)
            result = wikipedia.summary(request,sentences=2)
            print(result)
            speak(result)
        # elif "jarvis " in request:
        #     try:
        #         # Remove the trigger phrase and clean the user input
        #         request = request.replace("jarvis ai", "").strip()

        #         # Initialize the generative model and start a chat session
        #         model = genai.GenerativeModel("gemini-1.5-flash")
        #         chat = model.start_chat(
        #             history=[
        #                 {
        #                     "role": "user",
        #                     "parts": "Hi, your name is Jarvis. Answer all questions as if a Python library will speak what you write. Try to respond in 3 to 4 lines unless instructed otherwise.......... the name of your creator is moksh he is a tech student pursuing Bachelors in Artificial Intelligence and machine learning",
        #                 },
        #                 {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        #             ]
        #         )

        #         # Send the user's query to the model
        #         response = chat.send_message(request)

        #         # Print and speak the model's response
        #         print(f"Jarvis: {response.text}")
        #         speak(response.text)

        #     except Exception as e:
        #         # Error handling in case of any issues
        #         speak("I encountered an issue while processing your request. Please try again later.")
        #         print(f"Error: {e}")
        elif "jarvis" in request:
            try:
                # Initialize the Generative Model
                model = genai.GenerativeModel("gemini-1.5-flash")
                chat = model.start_chat(
                    history=[
                        {"role": "user", "parts": "hi your name is jarvis and now you have to answer all the question in such a manner that a python library will be speaking what you wrote try to answer in not more than 3 or 4 lines untill u r instructed to......... the name of your creator is moksh he is a tech student pursuing Bachelors in Artificial Intelligence and machine learning"},
                        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
                    ]
                )
                
                # Notify the user about entering chat mode
                speak("I am here to chat with you. Say 'stop' to end the conversation.")
                print("Chat mode started. Type 'stop' to exit.")

                while True:
                    # Capture user input
                    request = command().lower().strip()
                    
                    if "stop" in request:
                        speak("Exiting chat mode. Let me know if there's anything else I can do for you!")
                        break
                    
                    if request:
                        # Send the user's input to the model and get the response
                        response = chat.send_message(request)
                        speak(response.text)  # Speak the response
                        print(f"Jarvis: {response.text}")  # Print the response
                    else:
                        speak("I didn't catch that. Can you please repeat?")
            except Exception as e:
                speak("I encountered an issue while chatting. Please try again later.")
                print(f"Error: {e}")
        elif"generate image" in request:
            request=request.replace("generate image of","")
            speak("generating image of "+ request)
            prompt = request
            width = 1216
            height = 1574
            seed = 2482463691  # Random seed for image variation
            model = "flux"  # Specify the model (adjust if necessary)

            # Construct the image URL using parameters
            image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width={width}&height={height}&seed={seed}&model={model}"

            # Download the generated image
            download_image(image_url)
if __name__ == "__main__":
    main_process()