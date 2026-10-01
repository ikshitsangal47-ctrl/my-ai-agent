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

# Suppress ALSA / Audio warnings in terminal output
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
sys.stderr = open(os.devnull, 'w')

import speech_recognition as sr
import pyautogui
from playwright.sync_api import sync_playwright
import openpyxl
from pptx import Presentation

# Safe Text-To-Speech Engine Initialisation
try:
    import pyttsx3
    engine = pyttsx3.init()
except Exception:
    engine = None

def speak(text):
    sys.stdout.write(f"\n[Agent]: {text}\n")
    sys.stdout.flush()
    if engine:
        try:
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
        # Fallback to text input
        try:
            command = input("\nType your command > ")
            return command.lower().strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit()

def open_youtube(search_query=""):
    speak(f"Opening YouTube for search: '{search_query if search_query else 'Home'}'...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True) # Container friendly
            page = browser.new_page()
            url = f"https://www.youtube.com/results?search_query={search_query}" if search_query else "https://www.youtube.com"
            page.goto(url)
            speak(f"Page loaded successfully: {page.title()}")
            time.sleep(3)
            browser.close()
    except Exception as e:
        speak(f"Failed to open browser: {e}")

def create_excel_sheet():
    speak("Creating Excel spreadsheet...")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Agent Report"
    ws.append(["ID", "Task", "Status"])
    ws.append([1, "Voice Agent Setup", "Completed"])
    wb.save("Agent_Report.xlsx")
    speak("Excel sheet saved as 'Agent_Report.xlsx' in current directory!")

def create_presentation():
    speak("Creating PowerPoint presentation...")
    prs = Presentation()
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "AI Desktop Agent"
    slide.placeholders[1].text = "Automated Task Execution"
    prs.save("Agent_Presentation.pptx")
    speak("Presentation saved as 'Agent_Presentation.pptx' in current directory!")

def main():
    speak("Custom AI Desktop Agent is online and ready.")
    while True:
        command = listen_command()
        if not command:
            continue
            
        if "youtube" in command:
            query = input("Enter YouTube search query > ")
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
