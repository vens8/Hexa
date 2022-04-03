import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import pyaudio
import winsound

# Suggestions
'''
Make a User class and then two child classes Student & Teacher (depends on use case).
Store user details using file handling and add/update/delete attributes of users using voice commands
(by adding necessary if statements)

Can use the user objects to login and give more personalised responses.

Instead of infinitely running While True for listening to commands, limit to 2-3. So, stop when there's no
valid command consecutively for 2-3 times (using boolean, assert). 
'''


class User:
    def __init__(self):
        self.name = None
        self.nickname = None
        self.age = None
        self.number = None


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            winsound.PlaySound("listenAlert.wav", winsound.SND_FILENAME)  # Play sound before listening
            print('listening...')
            listener.adjust_for_ambient_noise(source, 2.5)
            listener.pause_threshold = 1
            voice = listener.listen(source, timeout=10, phrase_time_limit=10)
            # voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if command:
                command = command.lower()
                speak(command)
                return command
    except sr.UnknownValueError:
        return


def run_hexard():
    command = take_command()  # Take speech input from user
    try:
        if command:
            print(command)
            print("Processing your command...")
            if 'play' in command:
                song = command.replace('play', '')
                speak('Now playing ' + song)
                pywhatkit.playonyt(song)
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                speak('Current time is ' + time)
            elif 'who is' in command:
                person = command.replace('who is', '')
                info = wikipedia.summary(person, 1)
                print(info)
                speak(info)
            elif 'what is' in command:
                speak("Searching Wikipedia...")
                thing = command.replace('what is', '')
                info = wikipedia.summary(thing, 1)
                print(info)
                speak(info)
            elif 'date' in command:
                speak('sorry, I have a headache')
            elif 'who are you' in command:
                speak("Wow, I thought you knew me. Well, I'm Hexard, nice to meet you.")
            elif 'are you single' in command:
                speak("Hehe, why do you ask? I am in a relationship with Siri. The male one tho.")
            elif 'joke' in command:
                speak(pyjokes.get_joke())
            elif 'bye' in command:
                speak("Aww, sad to see you go. Catch you later!")
            else:
                speak("I didn't seem to catch that, please say your command again.")
        else:
            speak("I didn't seem to catch that, please say your command again.")

    except TypeError:
        print("Type Error")
        speak("I didn't seem to catch that, please say your command again.")


def reply():  # Test
    global query

    # Logic for executing tasks based on query
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        query = query.replace("search", "")
        query = query.replace("for", "")
        results = wikipedia.summary(query, sentences=1)
        speak(f'According to Wikipedia, {results}')

    elif 'open youtube' in query:
        speak('Opening Youtube')
        webbrowser.open("https://youtube.com")

    elif 'open stack overflow' in query:
        speak('Opening StackOverflow')
        webbrowser.open("https://stackoverflow.com")

    elif 'what' in query and 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, The time is {strTime}")

    elif 'how are you' or 'what\'s up' in query:
        speak('I am doing jolly good, sir.')


if __name__ == '__main__':
    while True:
        run_hexard()
