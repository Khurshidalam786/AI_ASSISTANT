import os
import re
import pyttsx3
import pyautogui
import pygetwindow as gw
import speech_recognition as sr
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


# Function to extract the minimize, close, and open commands from the user input
def extract_commands(command):
    minimize_match = re.search(r"(minimize|minimise)", command, re.IGNORECASE)
    close_match = re.search(r"(close|stop|terminate) (.+)", command, re.IGNORECASE)
    open_match = re.search(r"open (.+)", command)
    minimize_app = minimize_match.group(0).strip() if minimize_match else None
    close_app = close_match.group(2).strip() if close_match else None
    open_app = open_match.group(1).strip() if open_match else ""

    return minimize_app, close_app, open_app


# Function to minimize the active window
def minimize_window():
    active_window = gw.getActiveWindow()
    if active_window:
        active_window.minimize()
        time.sleep(1)
    else:
        speak("No active window found to minimize.")


# Function to close a specific application window by its title
def close_window(app_name):
    # Split the app_name into individual keywords
    keywords = [keyword.strip().lower() for keyword in app_name.split()]

    # Get the list of all windows with titles
    windows = gw.getWindowsWithTitle("")

    for window in windows:
        # Check if any keyword matches part of the window title
        if any(keyword in window.title.lower() for keyword in keywords):
            try:
                # Activate and close the window
                window.activate()  # Ensure the window is in focus
                window.close()  # Close the window
                speak(f"Closed {window.title}")
                return True
            except Exception as e:
                print(f"Failed to close {window.title}: {e}")
                speak(f"Failed to close {window.title}.")
                return False

    # If no matching window was found
    speak(f"No window matching {app_name} found.")
    return False


# Function to check if an application is open in the taskbar
def is_app_open_in_taskbar(app_name):
    keywords = [keyword.strip().lower() for keyword in app_name.split()]
    windows = gw.getWindowsWithTitle("")
    for window in windows:
        # Check if any keyword matches part of the window title
        if any(keyword in window.title.lower() for keyword in keywords):
            try:
                # Activate and close the window
                window.activate()  # Ensure the window is in focus
                speak(f"Activated {window.title}")
                return True
            except Exception as e:
                print(f"Failed to activate {window.title}: {e}")
                speak(f"Failed to activate {window.title}.")
                return False

    # If no matching window was found
    speak(f"No window matching {app_name} found.")
    return False


# Function to open an application from the taskbar or by searching
def open_application(app_name):
    if is_app_open_in_taskbar(app_name):
        return True
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
            minimize_app, close_app, open_app = extract_commands(command)
            if minimize_app:
                minimize_window()
            if open_app:
                open_application(open_app)
            if close_app:
                close_window(close_app)
            else:
                speak("Please specify the application name to open or close.")


if __name__ == "__main__":
    main()
