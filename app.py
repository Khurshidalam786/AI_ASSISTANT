import os
import re
import speech_recognition as sr
import pyttsx3
import pyautogui
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Function to greet the user
def greet_user():
    speak("Hello! How can I assist you today?")


# Function to take voice commands from the user
def listen_for_command():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

    return ""


# Function to extract app name from command
def extract_app_name(command):
    match = re.search(r"open (.+)", command)
    if match:
        return match.group(1).strip()
    return ""


# Function to simulate pressing Win key, typing app name, and pressing Enter
def open_application(app_name):
    speak(f"Opening {app_name}")
    pyautogui.press("win")
    time.sleep(1)  # wait for the start menu to open
    pyautogui.write(app_name)
    time.sleep(1)  # wait for the search results to appear
    pyautogui.press("enter")


# Main function
def main():
    greet_user()
    while True:
        command = listen_for_command()
        if command:
            app_name = extract_app_name(command)
            if app_name:
                open_application(app_name)
            else:
                speak("Please specify the application name to open.")


if __name__ == "__main__":
    main()
