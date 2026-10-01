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
    except Exception as e:
        pass

import speech_recognition as sr
import pyttsx3
import pyautogui
from playwright.sync_api import sync_playwright
import openpyxl
from pptx import Presentation

# Initialize Text-To-Speech engine
engine = pyttsx3.init()

def speak(text):
    print(f"Agent: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Speech service is unavailable.")
            return ""
        except Exception:
            return ""

def open_youtube(search_query=""):
    speak("Opening YouTube...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        if search_query:
            page.goto(f"https://www.youtube.com/results?search_query={search_query}")
        else:
            page.goto("https://www.youtube.com")
        time.sleep(5)
        browser.close()

def create_excel_sheet():
    speak("Creating Excel spreadsheet...")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Agent Report"
    ws.append(["ID", "Task", "Status"])
    ws.append([1, "Voice Agent Setup", "Completed"])
    wb.save("Agent_Report.xlsx")
    speak("Excel sheet saved as Agent_Report.xlsx")

def create_presentation():
    speak("Creating PowerPoint presentation...")
    prs = Presentation()
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "AI Desktop Agent"
    subtitle.text = "Automated Task Execution"
    prs.save("Agent_Presentation.pptx")
    speak("Presentation saved as Agent_Presentation.pptx")

def main():
    speak("Custom AI Desktop Agent is online and ready.")
    while True:
        command = listen_command()
        
        if "youtube" in command:
            speak("What should I search on YouTube?")
            query = listen_command()
            open_youtube(query)
        elif "excel" in command or "sheet" in command:
            create_excel_sheet()
        elif "presentation" in command or "ppt" in command:
            create_presentation()
        elif "exit" in command or "stop" in command:
            speak("Shutting down agent. Goodbye!")
            sys.exit()

if __name__ == "__main__":
    main()
  
