import speech_recognition as sr
import pyttsx3
import subprocess
import os
import webbrowser
import pyautogui


# Initialize female voice engine 
engine = pyttsx3.init()
voices = engine.getProperty("voices")
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break

engine.setProperty("rate", 180)  # Increase speaking speed

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech(timeout=2, phrase_time_limit=3):
    """Listens for user speech and returns recognized text faster."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Faster noise adjustment
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return recognizer.recognize_google(audio).lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return None

# Open and Close Apps
def open_app(app_name):
    apps = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    }
    if app_name in apps:
        subprocess.Popen(apps[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"I couldn't find {app_name}.")

def close_app(app_name):
    processes = {
        "chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
    }
    if app_name in processes:
        os.system(f"taskkill /f /im {processes[app_name]}")
        speak(f"Closing {app_name}")
    elif "youtube" in app_name:
        speak("Closing YouTube tab")
        pyautogui.hotkey("ctrl", "w")
    else:
        speak(f"I couldn't find {app_name} running.")

# Play YouTube song
def play_song(song_name):
    search_query = song_name.replace(" ", "+")
    search_url = f"https://www.youtube.com/results?search_query={search_query}"
    
    speak(f"Searching YouTube for {song_name}")
    webbrowser.open(search_url)

# Open Websites
def open_website(site_name):
    websites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "instagram": "https://www.instagram.com",
        "github": "https://www.github.com"
    }
    if site_name in websites:
        webbrowser.open(websites[site_name])
        speak(f"Opening {site_name}")
    else:
        webbrowser.open(f"https://www.google.com/search?q={site_name}")
        speak(f"Searching Google for {site_name}")

# Main loop with wake word
def main():
    speak("Hey buddy.")

    while True:
        wake_word = recognize_speech(timeout=5, phrase_time_limit=4)
    
        if wake_word and "robin" in wake_word:
            print(f"Recognized: {wake_word}")

            command_handled = False

            if "open" in wake_word:
                app_name = wake_word.replace("robin", "").replace("open", "").strip()

                if "youtube" in app_name:
                    open_website("youtube")
                elif any(site in app_name for site in ["google", "facebook", "twitter", "instagram", "github"]):
                    open_website(app_name)
                else:
                    open_app(app_name)

                command_handled = True

            elif "close" in wake_word:
                app_name = wake_word.replace("robin", "").replace("close", "").strip()
                close_app(app_name)
            
                command_handled = True

            elif "play" in wake_word:
                song_name = wake_word.replace("robin", "").replace("play", "").strip()
                play_song(song_name)

                command_handled = True

            elif "exit" in wake_word or "stop" in wake_word:
                speak("Goodbye!")
                break

            if not command_handled:
                speak("sorry?")

if __name__ == "__main__":
    main()
