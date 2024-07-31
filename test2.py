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


# Function to extract the minimize and open commands from the user input
def extract_commands(command):
    minimize_match = re.search(r"minimize (.+)", command)
    open_match = re.search(r"open (.+)", command)

    minimize_app = minimize_match.group(1).strip() if minimize_match else None
    open_app = open_match.group(1).strip() if open_match else None

    return minimize_app, open_app


# Function to minimize the active window
def minimize_window():
    pyautogui.hotkey("win", "down")  # Minimize the active window
    time.sleep(1)


# Function to check if an application is open in the taskbar
def is_app_open_in_taskbar(app_name):
    # Take a screenshot of the taskbar
    taskbar_screenshot = pyautogui.screenshot(
        region=(0, pyautogui.size()[1] - 40, pyautogui.size()[0], 40)
    )
    taskbar_screenshot.save("taskbar.png")

    # Check if the application's icon is in the taskbar screenshot
    try:
        app_icon = pyautogui.locateCenterOnScreen(
            f"{app_name}.png", grayscale=True, confidence=0.8
        )
        return app_icon is not None
    except Exception as e:
        print(f"Error checking taskbar for {app_name}: {e}")
        return False


# Function to open an application from the taskbar or by searching
def open_application(app_name):
    if is_app_open_in_taskbar(app_name):
        speak(f"{app_name} is already open. Switching to {app_name}.")
        pyautogui.click(
            pyautogui.locateCenterOnScreen(
                f"{app_name}.png", grayscale=True, confidence=0.8
            )
        )
    else:
        speak(f"{app_name} is not open. Opening {app_name}.")
        pyautogui.press("win")
        time.sleep(1)  # Wait for the start menu to open
        pyautogui.write(app_name)
        time.sleep(1)  # Wait for the search results to appear
        pyautogui.press("enter")


# Main function
def main():
    greet_user()
    while True:
        command = listen_for_command()
        if command:
            minimize_app, open_app = extract_commands(command)
            if minimize_app:
                minimize_window()
            if open_app:
                open_application(open_app)
            else:
                speak("Please specify the application name to open.")


if __name__ == "__main__":
    main()
