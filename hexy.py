import datetime
import sys
import webbrowser
import winsound
from os.path import abspath

import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *

# from PySide2.QtGui import *

# Suggestions
'''
Make a User class and then two child classes Student & Teacher (depends on use case).
Store user details using file handling and add/update/delete attributes of users using voice commands
(by adding necessary if statements)

Can use the user objects to login and give more personalised responses.

Instead of infinitely running While True for listening to commands, limit to 2-3. So, stop when there's no
valid command consecutively for 2-3 times (using boolean, assert). 

Note: Might have to change the name of the voice assistant as 'Hexard' is not being recognised.
'''

flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female Voice


class Hexa:
    def __init__(self):
        pass

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def wish(self):
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            return "good morning"
        elif 12 <= hour < 18:
            return "good afternoon"
        else:
            return "good night"

    def take_command(self):
        try:
            with sr.Microphone() as source:
                print('listening...')
                winsound.PlaySound("listenAlert.wav", winsound.SND_FILENAME)  # Play sound before listening
                listener.adjust_for_ambient_noise(source, 2.5)
                listener.pause_threshold = 1  # Check these parameters
                voice = listener.listen(source, timeout=10, phrase_time_limit=10)
                # voice = listener.listen(source)
                command = listener.recognize_google(voice)
                if command:
                    command = command.lower()
                    # self.speak(command)
                    return command
        except sr.UnknownValueError:
            return

    def run_hexard(self, window):
        command = self.take_command()  # Take speech input from user
        try:
            assert type(command) is str
            print(type(command))
            if command:
                print(command)
                print("Processing your command...")
                if 'hexa' in command:
                    self.speak("Yes that's me, how may I help you?")
                    window.displayInfo("Yes that's me, how may I help you?")
                elif 'play' in command:
                    song = command.replace('play', '')
                    self.speak('Now playing ' + song)
                    window.displayInfo('Now playing ' + song)
                    pywhatkit.playonyt(song)
                elif 'on youtube' in command:
                    video = command.replace('on youtube', '')
                    self.speak('Now playing ' + video)
                    pywhatkit.playonyt(video)
                elif 'time' in command:
                    time = datetime.datetime.now().strftime('%I:%M %p')
                    self.speak('Current time is ' + time)
                elif 'hello' in command:
                    self.speak("Hey, what's up?")
                elif 'who is' in command:
                    person = command.replace('who is', '')
                    info = wikipedia.summary(person, 1)
                    print(info)
                    self.speak(info)
                elif 'your name' in command:
                    self.speak("Wow, I thought you knew me. Well, I'm Hexard, nice to meet you.")
                elif 'what is' in command:
                    self.speak("Searching Wikipedia...")
                    thing = command.replace('what is', '')
                    info = wikipedia.summary(thing, 1)
                    print(info)
                    self.speak(info)
                elif 'date' in command:
                    self.speak('sorry, I have a headache')
                elif 'who are you' in command:
                    self.speak("Wow, I thought you knew me. Well, I'm Hexard, nice to meet you.")
                elif 'how are you' in command:
                    self.speak("I'll be great as long as I'm electrically powered up, hehe. Thanks for asking though.")
                elif 'are you single' in command:
                    self.speak("Hehe, why do you ask? I am in a relationship with Siri. The male one tho.")
                elif 'joke' in command:
                    self.speak(pyjokes.get_joke())
                elif 'bye' in command:
                    self.speak("Aww, sad to see you go. Catch you later!")  # Add user name
                    exit(0)  # Deliberate exit
                    # return
                elif 'stop' in command:
                    self.speak(f"Okay, have a {self.wish()}. See ya!")
                    return True
                elif 'open youtube' in command:
                    self.speak('Opening Youtube')
                    webbrowser.open("https://youtube.com")
                elif 'good morning' in command or 'good afternoon' in command or 'good night' in command:
                    self.speak("So how's your day going so far? What are you up to?")
                else:
                    self.speak("I didn't seem to catch that, please say your command again.")
                    self.speak(f"Did you really mean to say {command}")

                    elseCommand = True  # To take further input from user as "yes or no" if required

            else:
                print("unrecognized")
                self.speak("I didn't seem to catch that, please say your command again.")
                # end += 1

        except AssertionError:
            print("Type Error")
            self.speak("I didn't seem to catch that, please say your command again.")
        return True

    def reply(self):  # Test
        global query

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            self.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            query = query.replace("search", "")
            query = query.replace("for", "")
            results = wikipedia.summary(query, sentences=1)
            self.speak(f'According to Wikipedia, {results}')

        elif 'open youtube' in query:
            self.speak('Opening Youtube')
            webbrowser.open("https://youtube.com")

        elif 'open stack overflow' in query:
            self.speak('Opening StackOverflow')
            webbrowser.open("https://stackoverflow.com")

        elif 'what' in query and 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"Sir, The time is {strTime}")

        elif 'how are you' or 'what\'s up' in query:
            self.speak('I am doing jolly good, sir.')

    def Start(self, window):
        return self.run_hexard(window)


class Ui_MainWindow(QMainWindow, object):
    def __init__(self):
        super().__init__()
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.backgroundImage = QtWidgets.QLabel(self.centralwidget)
        self.speak = QtWidgets.QLabel(self.centralwidget)
        self.infoLabel = QtWidgets.QLabel(self.centralwidget)
        self.infoLabel.setFont(QFont('Centauri', 5))
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setText("<font size=5 color='#00FFFF'>" + "Hey there, Hexa here!" + "</font>")
        self.gif = QMovie("button.gif")
        self.hexa = Hexa()
        self.hexa.speak(self.hexa.wish())

        MainWindow.setObjectName("MainWindow")
        self.setIcon()
        MainWindow.resize(1925, 1131)
        self.centralwidget.setObjectName("centralwidget")
        self.backgroundImage.setGeometry(QtCore.QRect(0, 0, 1921, 1131))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backgroundImage.sizePolicy().hasHeightForWidth())
        self.backgroundImage.setSizePolicy(sizePolicy)
        self.backgroundImage.setStyleSheet("QLabel{\n"
                                           "background-image: url('tech2.jpg');\n"
                                           "}")
        self.backgroundImage.setText("")
        self.backgroundImage.setObjectName("backgroundImage")
        self.speak.setGeometry(QtCore.QRect(830, 340, 341, 331))
        self.speak.setAutoFillBackground(False)
        self.speak.setStyleSheet("background-image: url('button.gif');\n"
                                 "")
        self.speak.setText("")
        # self.speak.setFlat(True)
        self.speak.setObjectName("speak")
        self.clickable(self.speak).connect(self.playHexa)
        self.infoLabel.setGeometry(QtCore.QRect(800, 720, 400, 100))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoLabel.sizePolicy().hasHeightForWidth())
        self.infoLabel.setSizePolicy(sizePolicy)
        self.infoLabel.setStyleSheet("background-image: url('infoLabel.png');")
        self.infoLabel.setObjectName("infoLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1925, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)
        self.speak.setMovie(self.gif)
        self.gif.stop()
        self.gif.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Hexa - Voice Assistant", "Hexa - Voice Assistant"))

    def clickable(self, widget):  # Promote label to button
        class Filter(QObject):
            clicked = pyqtSignal()

            def eventFilter(self, obj, event):
                if obj == widget:
                    if event.type() == QEvent.MouseButtonRelease:
                        if obj.rect().contains(event.pos()):
                            self.clicked.emit()
                            # The developer can opt for .emit(obj) to get the object within the slot.
                            return True

                return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def setIcon(self):
        window_icon = QIcon()
        window_icon.addFile('icon.png', QtCore.QSize(32, 32))
        self.setWindowIcon(app_icon)

    def startGif(self):
        self.speak.setMovie(self.gif)
        self.gif.stop()
        self.gif.start()

    def playHexa(self):
        print("Entered")
        # self.gif.setCacheMode(QMovie.CacheAll)
        self.startGif()
        self.hexa.Start(self)
        return

    def displayInfo(self, text):
        self.infoLabel.setText("<font size=5 color='#00FFFF'>" + text + "</font>")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QIcon()
    app_icon.addFile('icon.png', QtCore.QSize(32, 32))
    app.setWindowIcon(app_icon)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    MainWindow.showMaximized()
    sys.exit(app.exec_())