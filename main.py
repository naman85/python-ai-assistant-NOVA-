import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from googleapiclient.discovery import build

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "7dc0c60be8e143ac8742fe2c02b03762"


YOUTUBE_API_KEY = "AIzaSyC_71x6VcwdM5HrsJNA0s8Cq8hLMuVGHFM"


def speak(text, min_words=50):
    words = text.split()
    if len(words) <= min_words:
        short_text = text
    else:
        short_text = " ".join(words[:min_words])
        for word in words[min_words:]:
            short_text += " " + word
            if word.endswith(('.', '!', '?')):
                break
    engine.say(short_text)
    engine.runAndWait()

def aiProcess(command):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": f"Answer briefly in 4-5 sentences: {command}",
                "stream": False
            }
        )
        return response.json()['response']
    except Exception as e:
        print("Ollama error:", e)
        return "There was an error talking to the AI model"

def youtube_search(query):
    """Searches for a YouTube video and returns the URL of the first result."""
    try:
        # Build the YouTube API service object.
        youtube_service = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        # Make the search request.
        request = youtube_service.search().list(
            q=query,
            part="snippet",
            maxResults=1,
            type="video"
        )
        response = request.execute()

        # Extract the video ID and construct the URL.
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        else:
            return None 
        

    except Exception as e:
        print(f"Youtube error: {e}")
        return None

def processCommand(c):
    print(f"Processing command: {c}")

    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")

    
    

    elif c.lower().startswith("play"):
        song_query = c.lower().replace("play", "").strip()
        if song_query:
            speak(f"Searching for {song_query} on YouTube.")
            video_url = youtube_search(song_query)
            if video_url:
                webbrowser.open(video_url)
                speak(f"Playing {song_query} on YouTube.")
            else:
                speak("I couldn't find that video on YouTube.")
        else:
            speak("Please tell me what you would like to play.")

    elif "news" in c.lower() or "tell me news" in c.lower():
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
            print(f"Fetching news from: {url}")
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if not articles:
                    speak("No news articles found")
                    return
                
                speak("Here are the latest news headlines")
                for i, article in enumerate(articles[:5]):
                    if article['title']:
                        speak(f"Headline {i+1}: {article['title']}")
                    else:
                        speak("No title for this article")
            else:
                speak(f"Failed to fetch news. Status code: {r.status_code}")
        except Exception as e:
            print(f"News API error: {e}")
            speak("Speak, I encountered an error while fetching the news") 

    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Nova....")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listeninging...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            word = r.recognize_google(audio)
            if(word.lower() == "nova"):
                speak("Ya")
                with sr.Microphone() as source:
                    print("Nova active...")
                    audio = r.listen(source, timeout=8, phrase_time_limit=10)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))