import speech_recognition as sr
import os


def greet_user():
    print("Hello! How can I assist you today?")


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


def execute_command(command):
    if "open notepad" in command:
        print("Opening Notepad...")
        os.system("notepad.exe")


def main():
    greet_user()
    command = listen_for_command()
    execute_command(command)


if __name__ == "__main__":
    main()
