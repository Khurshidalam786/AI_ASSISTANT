import pygetwindow as gw
import psutil
import re


def close_application(app_name):
    windows = gw.getWindowsWithTitle("")

    for window in windows:
        if app_name.lower() in window.title.lower():
            try:
                # Try to close the window
                window.close()
                print(f"Closed {window.title}")
                return True
            except Exception as e:
                print(f"Failed to close {window.title}: {e}")
                return False
    print(f"{app_name} not found in visible windows.")
    return False


def extract_commands(command):
    close_match = re.search(r"close (.+)", command, re.IGNORECASE)
    if close_match:
        return close_match.group(1).strip()
    return None


if __name__ == "__main__":
    command = "close Google Chrome"  # Example command
    app_name = extract_commands(command)

    if app_name:
        closed = close_application(app_name)
        if not closed:
            print(f"Could not close {app_name}.")
    else:
        print("No valid command found.")
