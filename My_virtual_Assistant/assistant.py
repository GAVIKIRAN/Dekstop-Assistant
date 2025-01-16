import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import pyjokes
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the speech engine and other setups
engine = pyttsx3.init('sapi5')

def speak(text):
    engine.say(text)
    engine.runAndWait()

@app.route('/command', methods=['POST'])
def handle_command():
    user_query = request.form.get('query').lower()
    response = ""

    # Logic for executing tasks based on user query
    if "hello" in user_query or "hi" in user_query:
        response = "Hello! How can I help you?"
    elif 'joke' in user_query:
        response = pyjokes.get_joke()
    elif 'open youtube' in user_query:
        webbrowser.open("https://www.youtube.com/")
        response = "YouTube is open now"
        print("Youtube is open now")
    # Add more commands as needed

    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
