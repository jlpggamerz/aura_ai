from config import ASSISTANT_NAME
from voice.listener import Listener
from voice.speaker import Speaker
from core.commands import CommandRouter

class AuraAssistant:
    def __init__(self):
        self.speaker = Speaker()
        self.listener = Listener()
        self.router = CommandRouter()

    def run(self):
        self.speaker.say(
            f"Hello! I am {ASSISTANT_NAME}, your AI assistant. "
            "Say a command or type one below."
        )
        while True:
            try:
                command = self.listener.listen()
                if not command:
                    continue

                result = self.router.handle(command)
                if result.message:
                    self.speaker.say(result.message)

                if result.should_exit:
                    break

            except KeyboardInterrupt:
                self.speaker.say("Goodbye!")
                break
            except Exception as exc:
                print(f"[AURA ERROR] {exc}")
                self.speaker.say("Sorry, something went wrong. Please try again.")
