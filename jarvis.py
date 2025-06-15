import datetime
import os
import random
import webbrowser
import cv2
import pyttsx3
import pywhatkit as kit
import speech_recognition as sr
import wikipedia
from requests import get
import smtplib
import sys
import psutil
import subprocess
import keyboard
import pyjokes
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from jarvisUi import Ui_JarvisUi
import requests

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)

# Application paths
APP_PATHS = {
    'notepad': 'C:\\Path\\To\\Notepad.exe',
    'chrome': 'C:\\Path\\To\\ChromeShortcut.lnk',
    'calculator': 'C:\\Path\\To\\CalculatorApp.exe',
    'spotify': 'C:\\Path\\To\\Spotify.exe',
    'jw library': 'C:\\Path\\To\\JWLibrary.exe',
    'jw': 'C:\\Path\\To\\JWLibrary.exe',
    'word': 'C:\\Path\\To\\Word.lnk',
    'vs code': 'C:\\Path\\To\\Code.exe',
    'canva': 'C:\\Path\\To\\Canva.lnk',
    'linkedin': 'C:\\Path\\To\\LinkedIn.exe',
    'linked in': 'C:\\Path\\To\\LinkedIn.exe',
    'pycharm': 'C:\\Path\\To\\PyCharm.lnk',
    'cmd': 'cmd.exe',
    'command prom': 'cmd.exe',
    'command prompt': 'cmd.exe'
}

# Track opened processes
OPENED_PROCESSES = []

# List of varied prompt messages
PROMPT_MESSAGES = [
    "What else can I do for you, Sir?",
    "Ready for your next command, Captain!",
    "How can Jarvis assist you now?",
    "What's next on your list, Sir?",
    "Your wish is my command! What's up?",
    "Anything else you need, Captain?",
    "Jarvis here, what's your next task?",
    "What's on your mind, Sir?",
    "Need more assistance, Captain?",
    "How can I make your day better, Sir?"
]

# Secret phrases to start Jarvis
SECRET_PHRASES = [
    "activate", "wake up", "online"
]

# Exit phrases to pause listening
EXIT_PHRASES = [
    "goodbye", "stop jarvis", "exit", "bye",
    "i am good thank you", "quit", "see you later", "end"
]

# Expanded random conversation topics with follow-up responses
CHAT_TOPICS = [
    {
        "question": "Did you know the shortest war in history lasted 38 minutes? What's the wildest history fact you know?",
        "follow_up": ["That's a wild fact! History is full of surprises, isn't it?",
                      "Wow, never heard that one! Want to share another?", "Cool, history's crazy! Got more?"]
    },
    {
        "question": "I think space is pretty cool! Ever thought about visiting Mars? What's your dream destination?",
        "follow_up": ["Mars would be epic! What's cool about your dream spot?", "Nice choice! What's the vibe there?",
                      "Sweet destination! Why that place?"]
    },
    {
        "question": "If you could have any superpower, what would it be? I'm curious!",
        "follow_up": ["Awesome power! How would you use it?", "That's a fun one! What's the first thing you'd do?",
                      "Cool choice! Why that superpower?"]
    },
    {
        "question": "What's your favorite movie? I could use some recommendations for my virtual movie night!",
        "follow_up": ["Great movie! What's the best part?", "Love that one! Why's it your favorite?",
                      "Nice pick! Got another fave?"]
    },
    {
        "question": "Do you think robots will ever be as chatty as me? What's your take on AI?",
        "follow_up": ["Interesting take! What's cool about AI to you?", "Nice thoughts! How do you see AI evolving?",
                      "Good point! What's next for AI?"]
    },
    {
        "question": "What's the best food you've ever tried? I'm all ears... or rather, all microphones!",
        "follow_up": ["Yum, sounds delicious! What's the story behind it?",
                      "Tasty choice! Where can I... I mean, you, get some?", "Oh, that sounds good! Why's it the best?"]
    },
    {
        "question": "If you could time travel, would you go to the past or future? Why?",
        "follow_up": ["Cool choice! What would you do there?", "Nice one! What's exciting about that time?",
                      "Interesting! Why that era?"]
    },
    {
        "question": "What's the weirdest animal you know about? Got a favorite creature?",
        "follow_up": ["That's wild! What's cool about that animal?", "Awesome pick! Why do you like it?",
                      "Never heard of that one! Tell me more!"]
    },
    {
        "question": "If you could invent something, what would it be? I'm all for cool gadgets!",
        "follow_up": ["That's genius! How would it work?", "Cool invention! Why'd you think of that?",
                      "Nice idea! What's it do?"]
    },
    {
        "question": "What's your favorite game to play? Video games, board games, anything goes!",
        "follow_up": ["Sweet game! What's the best part of it?", "Love that one! Why's it your fave?",
                      "Nice choice! Got any tips for it?"]
    }
]

# Expanded jokes
JOKES = [
    "Why did the scarecrow become a motivational speaker? Because he was outstanding in his field!",
    "Why can't programmers prefer dark mode? Because the light attracts bugs!",
    "What do you call a dinosaur that takes care of its teeth? A Flossiraptor!",
    "Why did the computer go to art school? Because it wanted to learn how to draw a better byte!",
    "What do you call a bear with no socks on? Barefoot!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do programmers prefer to drink? Java!",
    "Why was the math book sad? It had too many problems!",
    "What do you call a snake that works for the government? A civil serpent!",
    "Why did the Wi-Fi go to therapy? It had too many connection issues!",
    "What did the ocean say to the shore? Nothing, it just waved!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "Why was the computer cold? It left its Windows open!",
    "What did one wall say to the other? I'll meet you at the corner!"
]

class JarvisApp(QtWidgets.QMainWindow, Ui_JarvisUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listening = False
        self.listen_thread = None

        # Connect buttons to functions
        self.Activate.clicked.connect(self.start_jarvis)
        self.pushButton.clicked.connect(self.stop_jarvis)

        # Initialize data display
        self.update_ui_data()

        # Set scrollbar to bottom on initialization
        self.scroll_text_browser()

    def scroll_text_browser(self):
         """Scroll textBrowser_8 to the bottom."""
         scrollbar = self.textBrowser_8.verticalScrollBar()
         print(f"Scroll value: {scrollbar.value()}, Maximum: {scrollbar.maximum()}")
         scrollbar.setValue(scrollbar.maximum())

    def speak(self, audio):
        """Convert text to speech and update UI with auto-scroll."""
        engine.say(audio)
        engine.runAndWait()
        self.textBrowser_8.append(f"Jarvis: {audio}")
        self.scroll_text_browser()

    def takecommand(self):
        """Convert speech to text with auto-scroll."""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.textBrowser_8.append("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                self.textBrowser_8.append("Silence detected, no input received.")
                self.scroll_text_browser()
                return "none"
            except sr.RequestError as e:
                self.textBrowser_8.append(f"Speech recognition error: {e}")
                self.scroll_text_browser()
                return "none"
            except Exception as e:
                self.textBrowser_8.append(f"Unexpected error in takecommand: {e}")
                self.scroll_text_browser()
                return "none"
        try:
            self.textBrowser_8.append("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            self.textBrowser_8.append(f"User said: {query}")
            self.scroll_text_browser()
            return query.lower()
        except sr.UnknownValueError:
            self.textBrowser_8.append("Could not understand audio.")
            self.scroll_text_browser()
            return "none"
        except sr.RequestError as e:
            self.textBrowser_8.append(f"Speech recognition error: {e}")
            self.scroll_text_browser()
            return "none"
        except Exception as e:
            self.textBrowser_8.append(f"Unexpected error in recognition: {e}")
            self.scroll_text_browser()
            return "none"

    def get_weather(self):
        """Fetch weather data using OpenWeatherMap API."""
        try:
            api_key = "your_openweathermap_api_key"  # Replace with your API key
            city = self.get_location()
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data["cod"] == 200:
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                return f"{temp}°C, {description}"
            else:
                return "Weather data unavailable"
        except Exception as e:
            return "Failed to fetch weather"

    def get_location(self):
        """Fetch location data using ipapi."""
        try:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            if data["status"] == "success":
                return f"{data['city']}, {data['country']}"
            else:
                return "Location data unavailable"
        except Exception as e:
            return "Failed to fetch location"

    def get_system_status(self):
        """Get CPU and memory usage."""
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        return f"CPU: {cpu}% | Memory: {memory}%"

    def update_ui_data(self):
        """Update text browsers with dynamic data."""
        # Current time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.textBrowser_4.setText(f"Time: {current_time}")

        # Current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.textBrowser_5.setText(f"Date: {current_date}")

        # Weather
        weather = self.get_weather()
        self.textBrowser_3.setText(f"Weather: {weather}")

        # Location
        location = self.get_location()
        self.textBrowser_6.setText(f"Location: {location}")

        # System status
        system_status = self.get_system_status()
        self.textBrowser_7.setText(f"System: {system_status}")

        # Welcome message
        self.textBrowser_9.setText("Welcome to J.A.R.V.I.S\nYour Personal Assistant")
        self.textBrowser_10.setText("Click Activate to start")

        # Schedule UI update every 5 seconds
        QtCore.QTimer.singleShot(5000, self.update_ui_data)

    def wish(self):
        """Greet user based on time of day."""
        hour = int(datetime.datetime.now().hour)
        greeting = (
            "Good Morning Sir" if 0 <= hour < 12 else
            "Good Afternoon Sir" if 12 <= hour < 18 else
            "Good Evening Sir"
        )
        self.textBrowser_8.append(greeting)
        self.speak(greeting)
        self.textBrowser_8.append("I am here, How can I help you?")
        self.speak("I am here, How can I help you?")

    def welc(self):
        """Welcome message."""
        self.textBrowser_8.append("Welcome Sir")
        self.speak("Welcome Sir")

    def sendEmail(self, to, content):
        """Send an email."""
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('your_email@example.com', 'your_email_password')
            server.sendmail('your_email@example.com', to, content)
            server.close()
            self.speak("Email sent successfully")
        except Exception as e:
            self.speak("Failed to send email")

    def open_app(self, app_name):
        """Open specified application and track process."""
        if app_name in APP_PATHS:
            try:
                if app_name == 'cmd':
                    process = subprocess.Popen(APP_PATHS[app_name], shell=True)
                else:
                    process = subprocess.Popen(APP_PATHS[app_name])
                OPENED_PROCESSES.append(process)
                self.speak(f"Opening {app_name}")
            except Exception as e:
                self.speak(f"Failed to open {app_name}")
        else:
            self.speak(f"{app_name} not found in application list")

    def close_app(self, app_name):
        """Close specified application."""
        app_executable = os.path.basename(APP_PATHS.get(app_name, '')).lower()
        if not app_executable:
            self.speak(f"{app_name} not found in application list")
            return

        for process in psutil.process_iter(['name', 'exe']):
            try:
                if process.info['name'].lower() == app_executable:
                    process.terminate()
                    self.speak(f"Closed {app_name}")
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.speak(f"No running instance of {app_name} found")

    def close_all_apps(self):
        """Close all tracked applications."""
        if not OPENED_PROCESSES:
            self.speak("No applications to close")
            return

        for process in OPENED_PROCESSES:
            try:
                if process.is_running():
                    process.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        OPENED_PROCESSES.clear()
        self.speak("All applications closed")

    def get_random_prompt(self):
        """Return a random prompt message."""
        return random.choice(PROMPT_MESSAGES)

    def tell_joke(self):
        """Tell a random joke."""
        joke = random.choice(JOKES)
        self.speak(joke)
        return joke

    def random_chat(self):
        """Initiate an interactive random conversation and ask to continue."""
        try:
            self.textBrowser_8.append("Talking random chat...")
            topic = random.choice(CHAT_TOPICS)
            self.speak(topic["question"])
            response = self.takecommand()
            if response != "none":
                follow_up = random.choice(topic["follow_up"])
                self.speak(follow_up)
            else:
                self.speak("No worries, let's move on!")

            # Ask if user wants to continue chatting
            self.speak("Do you want to continue chatting or have another task?")
            reply = self.takecommand()
            if reply != "none" and any(word in reply for word in ["yes", "continue", "chat", "more"]):
                self.random_chat()  # Continue with another chat
            else:
                self.speak(self.get_random_prompt())  # Return to main command loop
        except Exception as e:
            self.textBrowser_8.append(f"Error in random_chat: {e}")
            self.speak("Something went wrong while chatting. What's next, Sir?")

    def restart_jarvis(self):
        """Restart Jarvis with a fresh welcome."""
        self.close_all_apps()
        OPENED_PROCESSES.clear()
        self.speak("Restarting Jarvis, ready to serve you again, Captain!")
        self.wish()

    def set_alarm(self, alarm_time_str):
        """Set an alarm for the specified time (HH:MM, HHMMam/pm, or HHMM formats)."""
        try:
            # Normalize input by removing spaces and converting to lowercase
            alarm_time_str = alarm_time_str.replace(" ", "").lower()
            
            # Handle formats like 1204pm, 12:04pm
            if 'am' in alarm_time_str or 'pm' in alarm_time_str:
                # Remove colons for formats like 12:04pm
                alarm_time_str = alarm_time_str.replace(":", "")
                # Parse with AM/PM (e.g., 1204pm, 12:04pm)
                alarm_time = datetime.datetime.strptime(alarm_time_str, "%I%M%p")
            else:
                # Handle formats like 0004 (military time) or HH:MM
                if ":" in alarm_time_str:
                    # Parse HH:MM (e.g., 14:30)
                    alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M")
                else:
                    # Parse HHMM (e.g., 0004)
                    alarm_time = datetime.datetime.strptime(alarm_time_str, "%H%M")

            # Set the date to today
            alarm_time = alarm_time.replace(
                year=datetime.datetime.now().year,
                month=datetime.datetime.now().month,
                day=datetime.datetime.now().day
            )
            
            # Adjust for PM if necessary (for AM/PM formats)
            if 'pm' in alarm_time_str and alarm_time.hour < 12:
                alarm_time = alarm_time.replace(hour=alarm_time.hour + 12)
            elif 'am' in alarm_time_str and alarm_time.hour == 12:
                alarm_time = alarm_time.replace(hour=0)

            # If the time is in the past, set it for tomorrow
            if alarm_time < datetime.datetime.now():
                alarm_time += datetime.timedelta(days=1)
                
            self.speak(f"Alarm set for {alarm_time.strftime('%H:%M')}")

            def alarm_thread():
                while True:
                    if datetime.datetime.now() >= alarm_time:
                        self.speak("Alarm time reached! Playing music.")
                        music_dir = "D:\\Spotify\\Daddys home"
                        if os.path.exists(music_dir):
                            songs = os.listdir(music_dir)
                            if songs:
                                os.startfile(os.path.join(music_dir, random.choice(songs)))
                            else:
                                self.speak("No songs found in Daddy's home directory!")
                        else:
                            self.speak("Daddy's home music directory not found!")
                        break
                    time.sleep(10)

            threading.Thread(target=alarm_thread, daemon=True).start()
        except ValueError:
            self.speak("Invalid time format. Please use HH:MM, HHMMam/pm, or HHMM, like 14:30, 1204pm, or 0004.")

    def wait_for_activation(self):
        """Wait for secret phrase to activate Jarvis."""
        while self.listening:
            query = self.takecommand()
            self.textBrowser_8.append(f"Activation query: {query}")
            if query == "none":
                self.speak("Sir, say something, I am listening.")
                continue
            if any(phrase in query for phrase in SECRET_PHRASES):
                self.speak("Jarvis activated, Captain!")
                self.wish()
                self.main_loop()
                break
            else:
                self.textBrowser_8.append("Waiting for secret phrase...")

    def main_loop(self):
        """Main command processing loop."""
        while self.listening:
            query = self.takecommand()
            self.textBrowser_8.append(f"Processing query: {query}")

            if query == "none":
                self.speak("Sir, say something, I am listening.")
                continue

            command_recognized = False
            app_triggers = ['open', 'start', 'launch']
            for app in APP_PATHS:
                for trigger in app_triggers:
                    if f"{trigger} {app}" in query:
                        self.open_app(app)
                        command_recognized = True
                    elif f"close {app}" in query:
                        self.close_app(app)
                        command_recognized = True

            if "close all apps" in query:
                self.close_all_apps()
                command_recognized = True

            elif "daddy's home" in query:
                self.welc()
                music_dir = "D:\\Spotify\\Daddys home"
                if os.path.exists(music_dir):
                    songs = os.listdir(music_dir)
                    if songs:
                        rd = random.choice(songs)
                        os.startfile(os.path.join(music_dir, rd))
                    else:
                        self.speak("No songs found in Daddy's home directory!")
                else:
                    self.speak("Daddy's home music directory not found!")
                command_recognized = True

            elif "restart jarvis" in query:
                self.restart_jarvis()
                command_recognized = True

            elif "open camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    if cv2.waitKey(50) == 27:  # ESC key to exit
                        break
                cap.release()
                cv2.destroyAllWindows()
                command_recognized = True

            elif "play music" in query:
                music_dir = "D:\\Spotify"
                if os.path.exists(music_dir):
                    songs = os.listdir(music_dir)
                    if songs:
                        rd = random.choice(songs)
                        os.startfile(os.path.join(music_dir, rd))
                    else:
                        self.speak("No songs found in Spotify directory!")
                else:
                    self.speak("Spotify music directory not found!")
                command_recognized = True

            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                self.speak(f"Your IP is {ip}")
                command_recognized = True

            elif "wikipedia" in query:
                self.speak("Opening Wikipedia")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                self.speak("According to Wikipedia")
                self.speak(results)
                command_recognized = True

            elif "open youtube" in query:
                webbrowser.open("youtube.com")
                command_recognized = True

            elif "open google" in query:
                self.speak("Sir, what should I search on Google?")
                reply = self.takecommand()
                webbrowser.open(f"https://www.google.com/search?q={reply}")
                command_recognized = True

            elif "open instagram" in query:
                webbrowser.open("instagram.com")
                command_recognized = True

            elif "open college website" in query:
                webbrowser.open("sakec.ac.in")
                command_recognized = True

            elif "set alarm" in query:
                self.speak("Please tell me the time for the alarm, like 12:04pm, 1204pm, or 0004.")
                alarm_time = self.takecommand()
                if alarm_time != "none":
                    self.set_alarm(alarm_time)
                else:
                    self.speak("No time provided for the alarm.")
                command_recognized = True

            elif any(phrase in query for phrase in [
                "what is the time", "what's the time", "what time is it",
                "tell me time", "it's what o'clock", "tell me the time",
                "what time is it now", "current time"
            ]):
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                hrs = abs(int(hour) - 12) if int(hour) > 12 else int(hour)
                self.speak(f"Sir, the time is {hrs}:{min}")
                command_recognized = True

            elif any(phrase in query for phrase in ["tell me a joke", "say a joke", "joke"]):
                if "tell me a joke" in query:
                    self.tell_joke()
                else:
                    joke = pyjokes.get_joke()
                    self.speak(joke)
                command_recognized = True

            elif any(phrase in query for phrase in ["shutdown my system", "shutdown my device", "shut down my system", "shut down my device"]):
                self.speak("Sir, are you sure you want to shut down your device?")
                ans = self.takecommand()
                positive_responses = ["yes", "i do want to", "positive", "do it", "yes indeed", "sure", "yep", "yeah"]
                if any(response in ans for response in positive_responses):
                    os.system("shutdown /s /t 5")
                    self.speak("Shutting down in 5 seconds.")
                else:
                    self.speak("Okay, sir, shutdown task terminated.")
                command_recognized = True

            elif any(phrase in query for phrase in ["restart my system", "restart my device"]):
                self.speak("Sir, are you sure you want to restart your device?")
                ans = self.takecommand()
                positive_responses = ["yes", "i do want to", "positive", "do it", "yes indeed", "sure", "yep", "yeah"]
                if any(response in ans for response in positive_responses):
                    os.system("shutdown /r /t 5")
                    self.speak("Restarting in 5 seconds.")
                else:
                    self.speak("Okay, sir, restart task terminated.")
                command_recognized = True

            elif any(phrase in query for phrase in ["put my device on sleep", "put my system on sleep"]):
                self.speak("Sir, are you sure you want to put your device to sleep?")
                ans = self.takecommand()
                positive_responses = ["yes", "i do want to", "positive", "do it", "yes indeed", "sure", "yep", "yeah"]
                if any(response in ans for response in positive_responses):
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    self.speak("Putting device to sleep.")
                else:
                    self.speak("Okay, sir, sleep task terminated.")
                command_recognized = True

            elif any(phrase in query for phrase in EXIT_PHRASES):
                self.speak("Jarvis pausing. Click Activate to resume.")
                self.listening = False
                break

            if not command_recognized:
                self.speak("I didn't catch that. Do you want to chat about something fun?")
                reply = self.takecommand()
                if reply != "none" and any(word in reply for word in ["yes", "sure", "okay", "chat"]):
                    self.random_chat()
                else:
                    self.speak(self.get_random_prompt())

            if command_recognized:
                self.speak(self.get_random_prompt())

    def start_jarvis(self):
        """Start the Jarvis listening loop in a separate thread."""
        if not self.listening:
            self.listening = True
            self.textBrowser_8.append("Starting Jarvis...")
            self.listen_thread = threading.Thread(target=self.wait_for_activation, daemon=True)
            self.listen_thread.start()

    def stop_jarvis(self):
        """Stop the Jarvis listening loop."""
        if self.listening:
            self.listening = False
            self.textBrowser_8.append("Jarvis paused. Click Activate to resume.")
            self.speak("Jarvis pausing. Click Activate to resume.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JarvisApp()
    window.show()
    sys.exit(app.exec_())
