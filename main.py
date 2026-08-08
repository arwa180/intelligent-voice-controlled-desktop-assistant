import os
import queue
import sys
import subprocess
import webbrowser
import time
import sounddevice as sd
import pyttsx3
import pyautogui
import pyperclip
from vosk import Model, KaldiRecognizer

# ==========================================
# 1. TEXT-TO-SPEECH (TTS) INITIALIZATION
# ==========================================
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate', 175)

voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

def speak(text):
    """Utility function to handle vocal outputs."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


# ==========================================
# 2. DESKTOP AUTOMATION ENGINE (CORE CONTROL)
# ==========================================
def execute_command(raw_text):
    """Maps recognized speech commands to system automation actions."""
    text = raw_text.lower().strip()
    
    # --- Command: Hello ---
    if "hello" in text or "hi" in text:
        speak("Hello! I am your personalized assistant. Ready to help you.")
        
    # --- Command: Open Notepad ---
    elif "open notepad" in text:
        speak("Launching the Notepad application immediately.")
        subprocess.Popen("notepad.exe")
        
    # --- Command: Open Calculator ---
    elif "open calculator" in text or "calculator" in text:
        speak("Opening the system calculator application.")
        subprocess.Popen("calc.exe")
        
    # --- Dynamic Command: Close [application_name] ---
    elif text.startswith("close ") and text != "close window":
        app_name = text.split("close ", 1)[1].strip()
        
        if app_name:
            if "notepad" in app_name:
                subprocess.Popen("taskkill /F /IM notepad.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                speak("Closing Notepad.")
            elif "calculator" in app_name or "calc" in app_name:
                # Force close all potential calculator processes and simulate Alt+F4 as backup
                subprocess.Popen("taskkill /F /IM Calculator.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.Popen("taskkill /F /IM CalculatorApp.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                pyautogui.hotkey('alt', 'f4')
                speak("Closing Calculator.")
            elif "browser" in app_name or "chrome" in app_name:
                # Target Google Chrome specifically for closing
                subprocess.Popen("taskkill /F /IM chrome.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                speak("Closing Chrome browser.")
            else:
                subprocess.Popen(f"taskkill /F /IM {app_name}.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                speak(f"Attempting to close {app_name}.")

    # --- Command: Show Image ---
    elif "show image" in text or "display image" in text:
        if os.path.exists("sample.png"):
            speak("Displaying the predefined image now.")
            os.startfile("sample.png")
        else:
            speak("Predefined image sample.png was not found in the project folder.")
            
    # --- Command: Copy This Text ---
    elif "copy this text" in text or "copy text" in text:
        predefined_string = "Automated text from offline voice assistant."
        pyperclip.copy(predefined_string)
        speak("Predefined text has been copied to your system clipboard.")
        
    # --- Command: Read Clipboard ---
    elif "read clipboard" in text:
        clipboard_content = pyperclip.paste()
        if clipboard_content.strip():
            speak(f"The clipboard contains: {clipboard_content}")
        else:
            speak("The clipboard is currently empty.")
            
    # --- Command: Paste Clipboard ---
    elif "paste clipboard" in text or "paste text" in text:
        speak("Simulating paste operation.")
        pyautogui.hotkey('ctrl', 'v')
        
    # --- Command: Close Active Window ---
    elif "close window" in text:
        speak("Closing the active window in two seconds.")
        time.sleep(2) 
        pyautogui.hotkey('alt', 'f4')
        
    # --- Command: Type [your text] ---
    elif "type" in text:
        words_to_type = text.split("type", 1)[1].strip()
        if words_to_type:
            speak(f"Typing out text: {words_to_type}")
            pyautogui.write(words_to_type, interval=0.05)
            
    # --- Command: Minimize ONLY the Active Window ---
    elif "minimize" in text:
        speak("Minimizing the current active window.")
        # Pressing Win + Down Arrow twice handles restoration down and then minimization smoothly
        pyautogui.hotkey('win', 'down')
        time.sleep(0.1)
        pyautogui.hotkey('win', 'down')
        
    # --- Command: Maximize Window ---
    elif "maximize window" in text or "maximize" in text:
        speak("Maximizing the currently active window.")
        pyautogui.hotkey('win', 'up')
        
    # --- Command: Switch Window ---
    elif "switch window" in text or "switch application" in text:
        speak("Cycling focus through open applications.")
        pyautogui.hotkey('alt', 'tab')
        
    # --- Command: Open Web Browser (Forces Google Chrome) ---
    elif "open web browser" in text or "open browser" in text or "open chrome" in text:
        speak("Launching Google Chrome browser.")
        # Explicit path execution to force Google Chrome instead of the default system browser
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        try:
            webbrowser.get(chrome_path).open("https://www.google.com")
        except Exception:
            # Fallback if Chrome path differs on your machine
            webbrowser.open("https://www.google.com")
        
    # --- Command: Search [query] (Forces Google Chrome) ---
    elif "search" in text:
        search_query = text.split("search", 1)[1].strip()
        if search_query:
            speak(f"Searching for {search_query} on Google Chrome.")
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            search_url = f"https://www.google.com/search?q={search_query}"
            try:
                webbrowser.get(chrome_path).open(search_url)
            except Exception:
                webbrowser.open(search_url)
            
    # --- Command: Take Screenshot ---
    elif "take screenshot" in text or "screenshot" in text:
        screenshot_name = f"screenshot_{int(time.time())}.png"
        pyautogui.screenshot(screenshot_name)
        speak(f"Screen captured successfully. Saved as {screenshot_name}")
        
    # --- Command: Exit Assistant ---
    elif "exit assistant" in text or "goodbye" in text or "exit" in text:
        speak("Goodbye! Gracefully stopping the automation engine.")
        return False
        
    return True


# ==========================================
# 3. SPEECH-TO-TEXT (STT) & LOOP INITIALIZATION
# ==========================================
if not os.path.exists("model"):
    print("Error: 'model' directory not found!")
    sys.exit(1)

model = Model("model")
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

# Welcome message on system startup
speak("System initialized successfully. Voice control is active.")

try:
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                            channels=1, callback=audio_callback):
        
        print("\n>>> Assistant Loop Running. Speak Commands... (Ctrl+C to Terminate)")
        
        while True:
            data = audio_queue.get()
            
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                
                if '"text" :' in result:
                    text_heard = result.split('"text" : "')[1].split('"')[0].strip()
                    
                    if text_heard:
                        print(f"User: {text_heard}")
                        keep_running = execute_command(text_heard)
                        if not keep_running:
                            break
                            
except KeyboardInterrupt:
    print("\n[System Interrupted Safely by User]")
except Exception as e:
    print(f"\n[Unexpected Error Encountered]: {e}")