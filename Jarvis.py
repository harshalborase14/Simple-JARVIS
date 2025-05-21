import pyttsx3
import speech_recognition as sr
import os
import webbrowser
from ollama import Client
import pywhatkit
import pyautogui
import time
import psutil
import requests
import getpass
import subprocess
import json
import os
import ctypes
import socket
from datetime import datetime
import requests
from pyfiglet import Figlet

memory_file = "memory.json"

#Jarvis Banner
def show_jarvis_banner():
    print('\n')
    banner = Figlet(font='banner3-D')
    # banner = Figlet(font='banner3')
    # banner = Figlet(font='banner4')
    print(banner.renderText('J A R V I S'))  

#startup greet
def startup_greet_and_status():
    
    # Load memory to access saved name
    memory = get_memory_data()
    
    speak(f"Hello {memory['name']}, booting up now.")

    # Greeting
    hour = datetime.now().hour
    if 5 <= hour < 12:
        speak(f"Good morning {memory['name']}! I hope you slept well. I am {memory['assistant_name']}, ready to help you.")
    elif 12 <= hour < 17:
        speak(f"Good afternoon {memory['name']}! Ready to do some work? I am {memory['assistant_name']}.")
    elif 17 <= hour < 21:
        speak(f"Good evening {memory['name']}! Hope your day was productive. {memory['assistant_name']} at your service.")
    else:
        speak(f"Good night {memory['name']}! Still grinding, huh? I'm {memory['assistant_name']}, always here for you.")

    # Date & Time
    date = datetime.now().strftime("%B %d, %Y")
    time_now = datetime.now().strftime("%I:%M %p")
    speak(f"Today's date is {date}, and the current time is {time_now}.")

    # Battery
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = "charging" if battery.power_plugged else "not charging"
        speak(f"Battery is at {percent} percent and it is {plugged}.")
    else:
        speak("I couldn't access the battery information.")

    # Internet status
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        speak("Internet connection is active.")
    except OSError:
        speak("There is no internet connection at the moment.")

# Load memory from file
def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            return json.load(f)
    return {"name": "", "history": []}

# Save memory to file
def save_memory(memory):
    with open(memory_file, "w") as f:
        json.dump(memory, f, indent=4)



# Initialize text-to-speech engine once
engine = pyttsx3.init()
engine.setProperty('rate', 165)  # Adjust speech speed

# Select female or Indian voice if available
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower() or "india" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        print(f"🎤 Using voice: {voice.name}")
        break

# Keep the Ollama client alive
client = Client()

def speak(text):
    print("🤖 Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def speak_local(text, lang='mr'):  # 'mr' = Marathi, 'hi' = Hindi
    tts = gTTS(text=text, lang=lang)
    filename = "local_voice.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def ask_password():
    speak("Please enter your password.")
    correct_password = "1234"  # password
    entered_password = getpass.getpass("🔐 Enter your password: ")
    if entered_password == correct_password:
        print("✅ Access granted.")
        return True
    else:
        print("❌ Incorrect password.")
        return False

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2) 
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("⏱️ Timeout! You didn't speak in time.")
            return ""

    try:
        print("🔍 Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"🧑 You said: {query}")
        return query
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Could not request results: {e}")
        return ""


    try:
        print("🔍 Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"🧑 You said: {query}")
        return query
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Could not request results: {e}")
        return ""

def ask_ollama(question):
    response = client.chat(
        model='mistral',
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Always answer in one short and simple sentence only, even if the question is complex."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response['message']['content']

#get data from memory.json
def get_memory_data():
    with open("memory.json", "r") as f:
        return json.load(f)

def update_memory_data(key, value):
    data = get_memory_data()
    data[key] = value
    with open("memory.json", "w") as f:
        json.dump(data, f, indent=4)

# exit jarvis
def exit_jarvis():
    current_hour = datetime.now().hour
    if 21 <= current_hour or current_hour < 5:
        speak("Good night! Have a sweet dream!")
    else:
        speak("Goodbye! Have a nice day!")
    exit()

def perform_action(command):

    # Convert command to lowercase for easier matching
    command = command.lower()

    # Remove the word 'jarvis' from command if spoken
    if command.startswith("jarvis"):
        command = command.replace("jarvis", "", 1).strip()

    
    if "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad.exe")

    elif "open chrome" in command:
        speak("Opening Chrome")
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(chrome_path)

    elif "open browser" in command:
        speak("Opening Microsoft edge browser")
        edge_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        os.startfile(edge_path)

    elif "open vs code" in command or "open visual studio code" in command:
        speak("Opening Visual Studio Code")
        os.system("code")

    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open my portfolio" in command:
        speak("Opening Your Portfolio")
        webbrowser.open("https://harshalborase14.github.io/Portfolio/")  # Replace with your portfolio link

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc.exe")

    elif "open coding" in command or "your coding" in command:
        speak("Okay")
        if ask_password():
            speak("Access Granted. I'm giving my coding to you.")
            folder_path = r"D:\VSCode-Python\Jarvis-2025-Python"  # 'r' is used for raw string
            os.system(f'code "{folder_path}"')  # VS Code la string command format madhe pathavla
        else:
            speak("Access denied.")

    elif "open task manager" in command:
        speak("Opening Task Manager.")
        os.system("taskmgr")

    elif "open file explorer" in command:
        speak("Opening File Explorer.")
        os.system("explorer")

    elif "make a note" in command or "sticky note" in command:
        speak("What should I write in the note?")
        note = listen()
        if note:
            speak("Saving your note.")
            file_path = "sticky_note.txt"
            with open(file_path, "w") as f:
                f.write(note)
            os.system(f"notepad {file_path}")
        else:
            speak("I didn't catch the note content.")

    elif "play" in command:
        query = command.replace("play", "").strip()
        if query:
            speak(f"Playing {query} on YouTube")
            pywhatkit.playonyt(query)
        else:
            speak("Please say what to play.")

    elif "search on youtube" in command:
        query = command.split("search on youtube")[-1].strip()
        if query:
            speak(f"Searching {query} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        else:
            speak("Please say what to search on YouTube.")

    elif "search for" in command:
        query = command.split("search for")[-1].strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")


    elif "what is your name" in command.lower():
        if memory["assistant_name"]:
            speak(f"My name is {memory['assistant_name']}, Your personal assistant.")
        else:
            speak("")


    elif "your favourite song" in command:
        query = "mechanical sundariye"
        speak("Playing my favorite song on YouTube")
        pywhatkit.playonyt(query)

    elif "shutdown" in command or "turn off" in command:
        speak("Okay")
        if ask_password():
            speak("Shutting down the system.")
            os.system("shutdown /s /t 1")
        else:
            speak("Access denied.")

    elif "shut down" in command:
        speak("Okay")
        if ask_password():
            speak("Shutting down the system.")
            os.system("shutdown /s /t 1")
        else:
            speak("Access denied.")

    elif "your ip address" in command or "my ip address" in command or "tell me your ip address" in command:
        try:
            ip = requests.get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")
        except:
            speak("Sorry, I couldn't fetch your IP address right now.")

    elif "battery percentage" in command or "how much battery" in command or "battery status" in command:
        battery = psutil.sensors_battery()
        percent = battery.percent
        is_plugged = battery.power_plugged

        status = "charging" if is_plugged else "not charging"
        speak(f"Battery is at {percent} percent and it is {status}.")

    elif "what is the date" in command or "today's date" in command or "tell me the date" in command:
        from datetime import datetime
        date = datetime.now().strftime("%B %d, %Y")  # e.g., April 10, 2025
        speak(f"Today's date is {date}")

    elif "what is the day" in command or "today's day" in command or "tell me the day" in command:
        from datetime import datetime
        day = datetime.now().strftime("%A")  # e.g., Thursday
        speak(f"Today is {day}")

    elif "what is the time" in command or "current time" in command or "tell me the time" in command:
        from datetime import datetime
        time = datetime.now().strftime("%I:%M %p")  # e.g., 09:42 PM
        speak(f"The current time is {time}")

    elif "my name is" in command:
        name = command.replace("my name is", "").strip().title()
        memory["name"] = name
        save_memory(memory)
        speak(f"Okay, I will remember your name is {name}")

    elif "what is my name" in command:
        if memory["name"]:
            speak(f"Your name is {memory['name']}")
        else:
            speak("I don't know your name yet. Please tell me.")

    elif "my previous commands" in command or "what did I say" in command or "what did i say" in command:
        if memory["history"]:
            speak("Here's what you said earlier:")
            for cmd in memory["history"][-5:]:  # last 5 commands
                print(f"📌 {cmd}")
                speak(cmd)
        else:
            speak("You haven't said anything yet.")

    elif "search file" in command or "find file" in command:
        speak("Which file are you looking for?")
        filename = listen()
        search_path = "D:\\"  # or user-specified
        found = False
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if filename.lower() in file.lower():
                    file_path = os.path.join(root, file)
                    os.startfile(file_path)
                    speak("File found and opened.")
                    found = True
                    break
            if found:
                break
        if not found:
            speak("Sorry, I couldn't find the file.")

    elif "remember that" in command:
        fact = command.replace("remember that", "").strip()
        memory["facts"] = memory.get("facts", []) + [fact]
        save_memory(memory)
        speak("Got it. I'll remember that.")

    elif "what did you remember" in command:
        facts = memory.get("facts", [])
        if facts:
            for f in facts:
                speak(f)
        else:
            speak("I haven't remembered anything yet.")

    elif "take screenshot" in command:
        speak("Taking screenshot...")
        screenshot = pyautogui.screenshot()
        filename = "screenshot.png"
        screenshot.save(filename)
        speak("Screenshot saved.")

    elif "open downloads folder" in command:
        path = os.path.expanduser("~/Downloads")
        os.startfile(path)
        speak("Opening Downloads folder.")

    elif "mute system" in command:
        pyautogui.press("volumemute")
        speak("System muted.")

    elif "increase volume" in command:
        for _ in range(10):
            pyautogui.press("volumeup")
        speak("Volume increased.")

    elif "decrease volume" in command:
        for _ in range(10):
            pyautogui.press("volumedown")
        speak("Volume decreased.")

    
    elif "exit" in command or "bye" in command:
        exit_jarvis()

    elif "current location" in command or "where am i" in command or "my location" in command:
        try:
            speak("Let me check your current location...")
            res = requests.get("http://ip-api.com/json/")
            data = res.json()

            city = data.get("city")
            region = data.get("regionName")
            country = data.get("country")
            zip_code = data.get("zip")
            isp = data.get("isp")

            location_info = f"You are in {city}, {region}, {country}, and your ISP is {isp}."
            speak(location_info)
        except Exception as e:
            speak("Sorry, I couldn't fetch your location right now.")
            print("❌ Error:", e)

    #new commnads
    elif "lock system" in command or "lock laptop" in command:
        speak("Locking the system.")
        ctypes.windll.user32.LockWorkStation()

    elif "sleep" in command:
        speak("Putting the system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "restart system" in command or "restart laptop" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")

    elif "hibernate" in command:
        speak("Hibernating the system.")
        os.system("shutdown /h")

    elif "turn off screen" in command or "turn off display" in command:
        speak("Turning off the display.")
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)

    else:
        if not command:
            return
        answer = ask_ollama(command)
        speak(answer)

    # ✅ Save command to history 
    memory["history"].append(command)
    save_memory(memory)

memory = load_memory()

# Main loop
if __name__ == "__main__":
    speak("Booting Up...Running diagnostics...")
    show_jarvis_banner()
    if ask_password():
        speak("Access granted.")
        # startup_greet_and_status()
        speak("How can I assist you today?")
        while True:
            command = listen()
            if command.strip().lower() in ['exit', 'quit', 'stop', 'bye']:
                speak("Goodbye! Have a nice day!")
                break
            elif command:
                perform_action(command)
    else:
        speak("Access denied. Shutting down.")
        exit()