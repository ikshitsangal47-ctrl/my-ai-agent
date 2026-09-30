import os
import sys
import time
import platform
import speech_recognition as sr
import pyttsx3
import pyautogui
from pptx import Presentation
from openpyxl import Workbook
from playwright.sync_api import sync_playwright

engine = pyttsx3.init()

def speak(text):
    print(f"Agent: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nSuno bhai, command do...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="hi-IN")
        print(f"Aapne kaha: {command}")
        return command.lower()
    except Exception:
        print("Aawaz samajh nahi aayi, wapas bolo.")
        return ""

def open_youtube(query=""):
    speak("YouTube open kar raha hoon...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.youtube.com")
        if query:
            page.fill("input[name='search_query']", query)
            page.press("input[name='search_query']", "Enter")
        time.sleep(5)

def create_excel():
    speak("Excel sheet bana raha hoon...")
    wb = Workbook()
    ws = wb.active
    ws.title = "Tasks"
    ws.append(["ID", "Task Name", "Status"])
    ws.append([1, "Auto Presentation", "Completed"])
    file_name = "Task_Sheet.xlsx"
    wb.save(file_name)
    speak(f"Sheet {file_name} ban gayi!")
    if platform.system() == "Windows":
        os.system(f"start excel {file_name}")

def create_presentation():
    speak("Presentation bana raha hoon...")
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "AI Automated Presentation"
    slide.placeholders[1].text = "Generated autonomously by Custom Agent"
    file_name = "presentation.pptx"
    prs.save(file_name)
    speak("Presentation ready hai!")
    if platform.system() == "Windows":
        os.system(f"start soffice --impress {file_name}")

def parse_and_execute(cmd):
    if "youtube" in cmd:
        q = cmd.replace("youtube", "").strip()
        open_youtube(q)
    elif "excel" in cmd or "sheet" in cmd:
        create_excel()
    elif "presentation" in cmd or "ppt" in cmd:
        create_presentation()
    else:
        speak("Command samajh nahi aayi. YouTube, Excel ya Presentation bolein.")

if __name__ == "__main__":
    speak("Custom AI Agent Started! Bolo kya karna hai?")
    while True:
        cmd = listen_command()
        if "exit" in cmd or "stop" in cmd:
            speak("Bye bhai!")
            break
        if cmd:
            parse_and_execute(cmd)
