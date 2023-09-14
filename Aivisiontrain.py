# Import necessary libraries
import os
import cv2
import pyttsx3
import speech_recognition as sr
import datetime
from requests import get
import webbrowser
import pywhatkit as kit
import sys
import openai
import random
import subprocess
import psutil
import signal
from config import apikey # Import API key from config file

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# Store chat history for OpenAI interaction
chat_history = ""

#/// The following section is from :-
#///OpenAI platform, 2023. OpenAI platform [online]. Openai.com.
#///Available from: https://platform.openai.com/playground [Accessed 14 Aug 2023].


# Function to have a conversation with OpenAI
def chat_with_openai(query):
    global chat_history

    openai.api_key = apikey
    chat_history += f"User: {query}\nAI Fitness Trainer: "

    # Generate AI response using OpenAI's API
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chat_history,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Speak the AI response and update chat history
    speak(response["choices"][0]["text"])
    chat_history += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]
#/// end of Citation

# Function to generate AI response for a specific prompt
def generate_ai_response(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"

    # Generate AI response using OpenAI's API
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=10,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]

    # Create a directory for OpenAI responses if it doesn't exist
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # Save AI response to a file
    response_filename = f"Openai/{''.join(prompt.split()).strip()}.txt"

    with open(response_filename, "w") as f:
        f.write(text)

# Check if a fitness-related keyword is present in the query
def is_fitness_keyword_present(query):
    fitness_keywords = [
        "workout", "exercise", "fitness", "gym", "muscle", "training",
        "weight", "cardio", "reps", "sets", "stretch", "run", "calories",
        "protein", "diet", "aerobic", "anaerobic", "barbell", "dumbbell",
        "kettlebell", "treadmill", "elliptical", "bodybuilding", "yoga",
        "pilates", "motivate", "spin", "crossfit", "motivation", "HIIT",
        "circuit", "swimming", "squat", "deadlift", "bench press", "pushup",
        "pullup", "lunge", "burpee", "jump rope", "marathon", "triathlon",
        "endurance", "strength", "flexibility"
    ]

    for keyword in fitness_keywords:
        if keyword in query:
            return True
    return False

# Function to execute the main tasks
def main_task_execution():
    wish_user()
    gym_process_pid = None

    while True:
        user_query = take_user_command().lower().replace("one", "1")

        # Check if the query starts with "fitness"
        if not user_query.startswith("fitness"):
            continue

        user_query = user_query[len("fitness "):]

        # Execute various tasks based on user queries
        if "open notepad" in user_query:
            open_notepad()

        elif "close notepad" in user_query:
            close_notepad()

        elif "open command prompt" in user_query:
            open_command_prompt()

        elif "open camera" in user_query:
            open_camera()

        elif "play music" in user_query:
            play_music()

        elif "ip address" in user_query:
            get_ip_address()

        elif "open youtube" in user_query:
            open_website("www.youtube.com")

        elif "open github" in user_query:
            open_website("www.github.com")

        elif "open google" in user_query:
            search_google()

        elif "play songs on youtube" in user_query:
            play_youtube_song()


        # Execute computer vision for bicep curls task
        elif "exercise" in user_query and ("one" in user_query or "1" in user_query):

            start_bicep_curls(gym_process_pid)


        elif "close" in user_query and ("one" in user_query or "1" in user_query):

            close_bicep_curls(gym_process_pid)

        # Execute computer vision for Jumping Jack task
        elif "exercise" in user_query and ("two" in user_query or "2" in user_query):

            start_jumping_jack(gym_process_pid)


        elif "close" in user_query and ("two" in user_query or "2" in user_query):

            close_jumping_jack(gym_process_pid)

        # Execute computer vision for squats task
        elif "exercise" in user_query and ("three" in user_query or "3" in user_query):

            start_squats(gym_process_pid)


        elif "close" in user_query and ("three" in user_query or "3" in user_query):

            close_squats(gym_process_pid)

        # Generate AI response for custom prompts
        elif "make" in user_query.lower():
            generate_ai_response(user_query)

        elif "sleep" in user_query:
            speak("Thank you for using me. Have a great day!")
            break

        else:
            if is_fitness_keyword_present(user_query):
                chat_with_openai(user_query)
            else:
                speak("I'm not knowledgeable about that.")


# Function to take user's voice command
def take_user_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, timeout=200, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")

    except Exception as e:
        print(e)
        return "none"

    query = query.lower()
    return query


# Function to speak text
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Function to greet the user based on the time of day
def wish_user():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour <= 12:
        speak("Good Morning")
    elif 12 < hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am your Fitness Trainer. Please tell me how can I help you.")


def open_notepad():
    npath = "C:\\WINDOWS\\system32\\notepad.exe"
    os.startfile(npath)


def close_notepad():
    speak("Okay sir, closing Notepad")
    os.system("taskkill /f /im notepad.exe")


def open_command_prompt():
    os.system("start cmd")


def open_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        cv2.imshow('webcam', img)
        key = cv2.waitKey(50)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def play_music():
    music_dir = "C:\\Users\\ASUS\\Music\\Test"
    songs = os.listdir(music_dir)
    random_song = random.choice(songs)
    os.startfile(os.path.join(music_dir, random_song))


def get_ip_address():
    ip = get('https://api.ipify.org').text
    speak(f"Your IP address is {ip}")


def open_website(url):
    webbrowser.open(url)


def search_google():
    speak("Sir, what should I search?")
    query = take_user_command().lower()
    webbrowser.open(f"https://www.google.com/search?q={query}")


def play_youtube_song():
    kit.playonyt("love story")


gym_process_pid = None

def start_bicep_curls(process_pid):
    global gym_process_pid

    if gym_process_pid is None or not psutil.pid_exists(gym_process_pid):
        gym_path = "D:\\Motion_detect\\AItrainer6.py"
        gym_process = subprocess.Popen(["python", gym_path])
        gym_process_pid = gym_process.pid
        speak("Get ready to do Bicep curls, Move 3 step Backwards")
    else:
        speak("Gym exercise is already open.")

def close_bicep_curls(process_pid):
    global gym_process_pid

    if gym_process_pid and psutil.pid_exists(gym_process_pid):
        os.kill(gym_process_pid, signal.SIGTERM)
        gym_process_pid = None
        speak("Closing Bicep curls exercise.")
    else:
        speak("Gym exercise is not open.")

def start_jumping_jack(process_pid):
    global gym_process_pid

    if gym_process_pid is None or not psutil.pid_exists(gym_process_pid):
        gym_path = "D:\\Motion_detect\\Aitrainer8.py"
        gym_process = subprocess.Popen(["python", gym_path])
        gym_process_pid = gym_process.pid
        speak("Get ready to do Jumping Jack. Move 3 step Backwards")
    else:
        speak("Gym exercise is already open.")

def close_jumping_jack(process_pid):
    global gym_process_pid

    if gym_process_pid and psutil.pid_exists(gym_process_pid):
        os.kill(gym_process_pid, signal.SIGTERM)
        gym_process_pid = None
        speak("Closing Jumping Jack exercise.")
    else:
        speak("Gym exercise is not open.")

def start_squats(process_pid):
    global gym_process_pid

    if gym_process_pid is None or not psutil.pid_exists(gym_process_pid):
        gym_path = "D:\\Motion_detect\\Aitrainer9.py"
        gym_process = subprocess.Popen(["python", gym_path])
        gym_process_pid = gym_process.pid
        speak("Get ready to do squats. Move 3 step Backwards")
    else:
        speak("Gym exercise is already open.")

def close_squats(process_pid):
    global gym_process_pid

    if gym_process_pid and psutil.pid_exists(gym_process_pid):
        os.kill(gym_process_pid, signal.SIGTERM)
        gym_process_pid = None
        speak("Closing squats exercise.")
    else:
        speak("Gym exercise is not open.")


# The following part of the code initializes variables and starts the main loop based on user commands
if __name__ == "__main__":
    while True:
        user_command = take_user_command()
        # Check if the user wants to initiate the main task execution
        if not user_command.startswith("fitness"):
            continue

        user_command = user_command[len("fitness "):]
        # Start/Stop actions based on user commands
        if "wake up" in user_command:
            main_task_execution()
        elif "bye" in user_command:
            speak("Thank you. Goodbye!")
            sys.exit()