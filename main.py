import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    command = None
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)

            if 'hexard' in command:
                command = command.replace('hexard', '')
                print(command)
    except:
        print("Microphone")
    return command


def run_hexard():
    command = take_command()  # Take speech input from user
    print(command)
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
    elif 'date' in command:
        speak('sorry, I have a headache')
    elif 'are you single' in command:
        speak('I am in a relationship with wifi')
    elif 'joke' in command:
        speak(pyjokes.get_joke())
    else:
        speak("I didn't seem to catch that, please say your command again.")


if __name__ == '__main__':
    run_hexard()
