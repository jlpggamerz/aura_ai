import speech_recognition as sr

class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.7

    def listen(self):
        typed = input("\nYou (press Enter for voice): ").strip()
        if typed:
            return typed

        try:
            with sr.Microphone() as source:
                print("AURA is listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)

            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()

        except Exception as exc:
            print(f"[Voice input unavailable] {exc}")
            return input("Type your command: ").strip().lower()
