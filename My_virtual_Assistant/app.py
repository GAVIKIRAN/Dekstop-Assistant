from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import webbrowser
import os
import pyttsx3
import subprocess
from newsapi import NewsApiClient
import wikipedia
import time
import pyjokes
import datetime


app = Flask(__name__)

#recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[0].id)




def speak(text):
    try:
        #engine.say(text)
        print(text)
        engine.runAndWait()
        return engine.say(text),text
    except Exception as e:
        print(f"Error speaking text: {str(e)}")
    return text

#function to get news
def get_news(category="general"):
    api_key = "0850dfd991564c0d8de1cb231ccf43c2"
    newsapi = NewsApiClient(api_key=api_key)
    try:
        top_headlines = newsapi.get_top_headlines(category=category, language='en', country='us')
        if top_headlines['status'] == 'ok':
            articles = top_headlines['articles'][:5]
            if articles:
                headlines = [f"Headline {i+1}: {article['title']}" for i, article in enumerate(articles)]
                for headline in headlines:
                    speak(headline)
                    print(headline)
                return "Fetched latest news."
            else:
                speak("No articles found.")
                return "No articles found."
        else:
            speak("Sorry, I couldn't fetch news at the moment.")
            return "Failed to fetch news."
    except Exception as e:
        speak(f"An error occurred: {str(e)}")
        return "An error occurred while fetching news."
    

def search_wikipedia(query):
    try:
        print('Searching Wikipedia...')
        results = wikipedia.summary(query, sentences=2)
        print("According to Wikipedia")
        
        return results
    except Exception as e:
        #speak(f"I couldn't find information on {query}")
        return f"No information found for {query}"  

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        return "Good morning! How can I help you?"
    elif 12 <= hour < 18:
        return "Good afternoon! How can I help you?"
    else:
        return "Good evening! How can I help you?"
# Function to open a website
def open_website(website):
    try:
        if "youtube" in website:
            webbrowser.open("https://www.youtube.com")
            #s=speak("Opening youtube")            
            return 
        
        elif "hello" in website:
            #speak("Hello how can i help you")
            return wish_me()

        elif "news" in website:
            return get_news()
        
        elif "wikipedia" in website:
            query = website.replace("wikipedia", "").strip()  # Remove 'wikipedia' from the input
            if query:
                return search_wikipedia(query)
            else:
                return "Please specify what to search on Wikipedia."
        
        elif "time" in website:
            response = f"Current time is {datetime.datetime.now().strftime('%I:%M %p')}"
            return response

        elif "date" in website:
            response = f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
            return response

        elif 'open excel' in website:
            open_application("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
            response = "Opening Microsoft Excel."
            return response

        elif 'open word' in website:
            open_application("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
            response = "Opening Microsoft Word."            
            return response

        elif 'open powerpoint' in website:
            open_application("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")
            response = "Opening Microsoft PowerPoint."
            return response
        elif 'joke' in website:
            response = pyjokes.get_joke()
            speak(response)
            
            #return response
            
            
        elif "open google" in website:
            webbrowser.open("https://www.google.com")
            return "Opening Google..."
        elif "open twitter" in website:
            webbrowser.open("https://www.twitter.com")
            return "Opening Twitter..."
    
        elif "open linkedin" in website:
            webbrowser.open("https://www.linkedin.com")
            return "Opening LinkedIn..."
        
        elif "open instagram" in website:
            webbrowser.open("https://www.instagram.com")
            return "Opening Instagram..."
        elif "open amazon" in website:
            webbrowser.open("https://www.amazon.com")
            return "Opening Amazon..."
        elif "open github" in website:
            webbrowser.open("https://www.github.com")
            return "Opening GitHub..."
        elif "open stackoverflow" in website:
            webbrowser.open("https://stackoverflow.com")
            return "Opening StackOverflow..."
        elif "open wikipedia" in website:
            webbrowser.open("https://www.wikipedia.org")
            return "Opening Wikipedia..."
        elif "open reddit" in website:
            webbrowser.open("https://www.reddit.com")
            return "Opening Reddit..."
        elif "open netflix" in website:
            webbrowser.open("https://www.netflix.com")
            return "Opening Netflix..."
        elif "open spotify" in website:
            webbrowser.open("https://www.spotify.com")
            return "Opening Spotify..."
        elif "open zoom" in website:
            webbrowser.open("https://zoom.us")
            return "Opening Zoom..."
        elif "open whatsapp" in website:
            webbrowser.open("https://web.whatsapp.com")
            return "Opening WhatsApp..."
        
        elif "facebook" in website:
            webbrowser.open("https://www.facebook.com")
            return "Opening Facebook..."
        
        elif 'open folder bg' in website:
            path = r'D:\BG'
            try:
                os.startfile(path)
                #speak("Opening the BG folder.")
                return "opening folder bg"
            except Exception as e:
                #speak(f"I couldn't open the folder: {e}")
                return f"Failed to open the folder: {e}"
            
        elif 'open new folder' in website:
            path = r'D:\New folder'
            try:
                os.startfile(path)
                #speak("Opening the BG folder.")
                return "opening new folder "
            except Exception as e:
                #speak(f"I couldn't open the folder: {e}")
                return f"Failed to open the folder: {e}"    
        else:
            return "Website not recognized"
    except Exception as e:
        return f"Error: {str(e)}"

def open_application(path):
    try:
        subprocess.Popen(path, shell=True)
        speak("Opening application.")
    except Exception as e:
        speak(f"I couldn't open the application. Error: {str(e)}")
# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle text input
@app.route('/open_website_text', methods=['POST'])
def open_website_text():
    website = request.form.get('website')
    result = open_website(website.lower())
    return jsonify({"message": result})

# Route to handle voice input
@app.route('/open_website_voice', methods=['POST'])
def open_website_voice():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for a command...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        result = open_website(command.lower())
        return jsonify({"message": result})
    except sr.UnknownValueError:
        return jsonify({"message": "Sorry, I could not understand the voice command."})
    except sr.RequestError:
        return jsonify({"message": "Sorry, the speech recognition service is down."})


@app.route('/start_virtual_mouse', methods=['POST'])
def start_virtual_mouse():
    # Start the hand gesture control script in a separate process
    try:
        subprocess.Popen(['python', 'virtual_mouse.py'])  # Assuming the hand gesture control code is saved as virtual_mouse.py
        return jsonify({"message": "Virtual mouse started!"})
    except Exception as e:
        return jsonify({"message": f"Error starting virtual mouse: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)