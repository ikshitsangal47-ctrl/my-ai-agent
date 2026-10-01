import os
import sys
import time
import subprocess
import shutil
import speech_recognition as sr
import openpyxl
from pypdf import PdfReader
import pdfplumber

EXCEL_FILE = "Agent_Report.xlsx"

def speak_status(text):
    print(f"\n🤖 [AI Agent]: {text}")
    sys.stdout.flush()

def listen_continuous():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("\n🎙️  [Listening in background... Bolna shuru karo]")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=6)
            command = recognizer.recognize_google(audio)
            print(f"🗣️  You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("❌ Speech API Connection Error")
            return ""
        except Exception:
            return ""

# ==========================================
# 1. ANY APP LAUNCHER FEATURE (NO LIMITS)
# ==========================================
def launch_any_app(app_name):
    speak_status(f"Searching and opening application: '{app_name}'...")
    
    # Common App Mappings
    app_map = {
        "chrome": "google-chrome",
        "google chrome": "google-chrome",
        "firefox": "firefox",
        "browser": "firefox",
        "terminal": "gnome-terminal",
        "vscode": "code",
        "code": "code",
        "vs code": "code",
        "calculator": "gnome-calculator",
        "calc": "gnome-calculator",
        "text editor": "gedit",
        "notepad": "gedit",
        "files": "nautilus",
        "file manager": "nautilus",
        "spotify": "spotify",
        "vlc": "vlc",
        "settings": "gnome-control-center"
    }

    executable = app_map.get(app_name, app_name)
    
    # Check if command exists on system
    if shutil.which(executable):
        try:
            subprocess.Popen([executable])
            speak_status(f"Successfully launched {app_name}!")
            return
        except Exception as e:
            speak_status(f"Failed to launch {app_name}: {e}")
            return

    # Fallback to system-wide search using xdg or gtk-launch
    try:
        subprocess.Popen(["gtk-launch", executable], stderr=subprocess.DEVNULL)
        speak_status(f"Launched '{app_name}' via Desktop System Launcher.")
    except Exception:
        try:
            subprocess.Popen([executable], stderr=subprocess.DEVNULL)
            speak_status(f"Launched '{app_name}' successfully!")
        except Exception:
            speak_status(f"Application '{app_name}' not found on system. Make sure it's installed!")

# ==========================================
# 2. EXCEL AUTOMATION & DATA ENTRY
# ==========================================
def create_initial_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Voice Data"
    ws.append(["ID", "Voice Entry / Data", "Timestamp"])
    wb.save(EXCEL_FILE)

def open_excel_app():
    speak_status("Opening Excel Spreadsheet...")
    if not os.path.exists(EXCEL_FILE):
        create_initial_excel()
    subprocess.Popen(["xdg-open", EXCEL_FILE])

def add_voice_data_to_excel(raw_text):
    if not os.path.exists(EXCEL_FILE):
        create_initial_excel()

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    next_id = ws.max_row
    
    # Clean up command prefixes
    clean_data = raw_text
    for prefix in ["add data", "enter data", "write", "insert", "excel me dalo", "add"]:
        clean_data = clean_data.replace(prefix, "")
    clean_data = clean_data.strip().capitalize()
    
    if not clean_data:
        clean_data = raw_text

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    ws.append([next_id, clean_data, timestamp])
    wb.save(EXCEL_FILE)
    speak_status(f"Saved into Excel: Row {next_id} -> '{clean_data}'")

# ==========================================
# 3. PDF EXTRACTION TO EXCEL
# ==========================================
def process_pdf_to_excel():
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if not pdf_files:
        speak_status("No .pdf file found in the project folder! Drop a PDF first.")
        return

    pdf_path = pdf_files[0]
    speak_status(f"Reading and extracting PDF file: '{pdf_path}'...")
    
    text_content = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
    except Exception as e:
        speak_status(f"Error reading PDF: {e}")
        return

    full_text = "\n".join(text_content)
    
    if not os.path.exists(EXCEL_FILE):
        create_initial_excel()

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    
    ws.append([])
    ws.append(["--- PDF IMPORT ---", pdf_path, time.strftime("%Y-%m-%d %H:%M:%S")])
    
    lines_added = 0
    for line in full_text.split("\n"):
        if line.strip():
            lines_added += 1
            ws.append([lines_added, line.strip(), "PDF Data"])
            
    wb.save(EXCEL_FILE)
    speak_status(f"Successfully extracted {lines_added} lines from '{pdf_path}' into '{EXCEL_FILE}'!")

# ==========================================
# 4. MAIN AGENT ENGINE
# ==========================================
def main_agent_loop():
    speak_status("Custom AI Voice Desktop Agent Activated!")
    speak_status("Listening for voice commands in background...")
    
    while True:
        command = listen_continuous()
        if not command:
            continue
            
        # App Launcher Intent Trigger
        if "open " in command or "chalo " in command or "kholo " in command:
            if "excel" in command or "sheet" in command:
                open_excel_app()
            else:
                # Extract App Name dynamically
                app_name = command.replace("open", "").replace("kholo", "").replace("chalo", "").strip()
                launch_any_app(app_name)

        # Excel Data Entry Trigger
        elif any(k in command for k in ["add data", "enter", "write", "insert", "excel"]):
            add_voice_data_to_excel(command)

        # PDF Parse Trigger
        elif "pdf" in command or "read pdf" in command or "upload pdf" in command:
            process_pdf_to_excel()

        # Stop Trigger
        elif "stop" in command or "exit" in command or "bye" in command:
            speak_status("Shutting down AI Agent. Goodbye!")
            sys.exit()

if __name__ == "__main__":
    main_agent_loop()
