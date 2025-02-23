import sys
import speech_recognition as sr
import pyttsx3
import openai
#Force UTF-8 encoding (fix for UnicodeEncodeError)
sys.stdout.reconfigure(encoding='utf-8')
# Initialize OpenAI Client (Replace with your actual API key)
client = openai.OpenAI(api_key="YOUR_API_KEY")  

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user input using microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # 5 sec timeout
            command = recognizer.recognize_google(audio)
            print("🗣 You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("❌ Sorry, I couldn't understand.")
            return ""
        except sr.RequestError:
            print("⚠️ Error: Check your internet connection.")
            return ""
        except sr.WaitTimeoutError:
            print("⏳ No speech detected. Try again.")
            return ""

def chat_with_gpt(prompt):
    """Send user query to OpenAI GPT and return the response."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content  # Extract text response
    except openai.APIError as e:
        print(f"⚠️ OpenAI API error: {e}")
        return "Sorry, I am facing some technical issues."
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return "Something went wrong."

def main():
    """Main function to run the voice assistant."""
    speak("Hello, I am Jarvis. How can I assist you today?")
    while True:
        command = listen()
        if "exit" in command or "stop" in command:
            speak("Goodbye! Have a great day!")
            break
        elif command:
            response = chat_with_gpt(command)
            print("🤖 Jarvis:", response)
            speak(response)

if __name__ == "__main__":
    main()
