import os
import sys
import time

# Auto-handle GUI display and Xauthority for Linux/Docker environments
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":99"

xauth_path = os.path.expanduser("~/.Xauthority")
if not os.path.exists(xauth_path):
    try:
        open(xauth_path, "a").close()
    except Exception:
        pass

# Suppress ALSA / Audio warnings completely
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import speech_recognition as sr
import pyautogui
from playwright.sync_api import sync_playwright
import openpyxl
from pptx import Presentation

# Safe Text-To-Speech Initialization (Bypass pyttsx3 in Docker)
def speak(text):
    print(f"\n[Agent]: {text}")
    sys.stdout.flush()
    # Try TTS only if an audio card exists, else skip audio silently
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

def listen_command():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=3)
            command = recognizer.recognize_google(audio)
            return command.lower()
    except Exception:
        # Fallback to manual terminal input if mic fails or doesn't exist
        try:
            command = input("\nType your command > ")
            return command.lower().strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit()

def open_youtube(search_query=""):
    speak(f"Opening YouTube for search: '{search_query if search_query else 'Home'}'...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Headless mode for Docker/Virtual Display
            page = browser.new_page()
            url = f"https://www.youtube.com/results?search_query={search_query}" if search_query else "https://www.youtube.com"
            page.goto(url)
            speak(f"Page loaded successfully! Title: '{page.title()}'")
            time.sleep(3)
            browser.close()
    except Exception as e:
        speak(f"Browser automation error: {e}")

def create_excel_sheet():
    speak("Creating Excel spreadsheet...")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Agent Report"
    ws.append(["ID", "Task", "Status"])
    ws.append([1, "Voice Agent Setup", "Completed"])
    wb.save("Agent_Report.xlsx")
    speak("Excel sheet created successfully as 'Agent_Report.xlsx'!")

def create_presentation():
    speak("Creating PowerPoint presentation...")
    prs = Presentation()
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "AI Desktop Agent"
    slide.placeholders[1].text = "Automated Task Execution"
    prs.save("Agent_Presentation.pptx")
    speak("Presentation created successfully as 'Agent_Presentation.pptx'!")

def main():
    speak("Custom AI Desktop Agent is online and ready.")
    while True:
        command = listen_command()
        if not command:
            continue
            
        if "youtube" in command:
            try:
                query = input("Enter YouTube search query > ")
            except (EOFError, KeyboardInterrupt):
                break
            open_youtube(query)
        elif "excel" in command or "sheet" in command:
            create_excel_sheet()
        elif "presentation" in command or "ppt" in command:
            create_presentation()
        elif "exit" in command or "stop" in command:
            speak("Shutting down agent. Goodbye!")
            sys.exit()
        else:
            speak(f"Command '{command}' not recognized. Try 'youtube', 'excel', 'presentation', or 'exit'.")

if __name__ == "__main__":
    main()import os
import sys
import time

# Auto-handle GUI display and Xauthority for Linux/Docker environments
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":99"

xauth_path = os.path.expanduser("~/.Xauthority")
if not os.path.exists(xauth_path):
    try:
        open(xauth_path, "a").close()
    except Exception:
        pass

# Suppress ALSA / Audio warnings completely
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import speech_recognition as sr
import pyautogui
from playwright.sync_api import sync_playwright
import openpyxl
from pptx import Presentation

# Safe Text-To-Speech Initialization (Bypass pyttsx3 in Docker)
def speak(text):
    print(f"\n[Agent]: {text}")
    sys.stdout.flush()
    # Try TTS only if an audio card exists, else skip audio silently
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

def listen_command():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=3)
            command = recognizer.recognize_google(audio)
            return command.lower()
    except Exception:
        # Fallback to manual terminal input if mic fails or doesn't exist
        try:
            command = input("\nType your command > ")
            return command.lower().strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit()

def open_youtube(search_query=""):
    speak(f"Opening YouTube for search: '{search_query if search_query else 'Home'}'...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Headless mode for Docker/Virtual Display
            page = browser.new_page()
            url = f"https://www.youtube.com/results?search_query={search_query}" if search_query else "https://www.youtube.com"
            page.goto(url)
            speak(f"Page loaded successfully! Title: '{page.title()}'")
            time.sleep(3)
            browser.close()
    except Exception as e:
        speak(f"Browser automation error: {e}")

def create_excel_sheet():
    speak("Creating Excel spreadsheet...")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Agent Report"
    ws.append(["ID", "Task", "Status"])
    ws.append([1, "Voice Agent Setup", "Completed"])
    wb.save("Agent_Report.xlsx")
    speak("Excel sheet created successfully as 'Agent_Report.xlsx'!")

def create_presentation():
    speak("Creating PowerPoint presentation...")
    prs = Presentation()
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "AI Desktop Agent"
    slide.placeholders[1].text = "Automated Task Execution"
    prs.save("Agent_Presentation.pptx")
    speak("Presentation created successfully as 'Agent_Presentation.pptx'!")

def main():
    speak("Custom AI Desktop Agent is online and ready.")
    while True:
        command = listen_command()
        if not command:
            continue
            
        if "youtube" in command:
            try:
                query = input("Enter YouTube search query > ")
            except (EOFError, KeyboardInterrupt):
                break
            open_youtube(query)
        elif "excel" in command or "sheet" in command:
            create_excel_sheet()
        elif "presentation" in command or "ppt" in command:
            create_presentation()
        elif "exit" in command or "stop" in command:
            speak("Shutting down agent. Goodbye!")
            sys.exit()
        else:
            speak(f"Command '{command}' not recognized. Try 'youtube', 'excel', 'presentation', or 'exit'.")

if __name__ == "__main__":
    main()
