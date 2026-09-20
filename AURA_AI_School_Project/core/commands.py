from dataclasses import dataclass
from features.browser import Browser
from features.calculator import Calculator
from features.system import SystemTools
from features.time_date import TimeDate

@dataclass
class CommandResult:
    message: str = ""
    should_exit: bool = False

class CommandRouter:
    def __init__(self):
        self.browser = Browser()
        self.calculator = Calculator()
        self.system = SystemTools()
        self.clock = TimeDate()

    def handle(self, command: str) -> CommandResult:
        c = command.lower().strip()

        if c in {"exit", "quit", "stop", "goodbye", "aura stop"}:
            return CommandResult("Goodbye! AURA is going offline.", True)

        if "time" in c:
            return CommandResult(self.clock.time())

        if "date" in c or "today" in c:
            return CommandResult(self.clock.date())

        if c.startswith("calculate "):
            expression = c.replace("calculate ", "", 1)
            return CommandResult(self.calculator.calculate(expression))

        if "open youtube" in c:
            self.browser.open("https://www.youtube.com")
            return CommandResult("Opening YouTube.")

        if "open google" in c:
            self.browser.open("https://www.google.com")
            return CommandResult("Opening Google.")

        if "open github" in c:
            self.browser.open("https://github.com")
            return CommandResult("Opening GitHub.")

        if "search" in c:
            query = c.replace("search", "", 1).replace("for", "", 1).strip()
            if query:
                self.browser.search(query)
                return CommandResult(f"Searching the web for {query}.")
            return CommandResult("Please tell me what you want me to search for.")

        if "open calculator" in c:
            self.system.open_calculator()
            return CommandResult("Opening calculator.")

        if "open notepad" in c:
            self.system.open_notepad()
            return CommandResult("Opening Notepad.")

        if c in {"hello", "hi", "hey", "hello aura", "hey aura"}:
            return CommandResult("Hello! I am AURA. How can I help you?")

        if "who are you" in c or "what are you" in c:
            return CommandResult(
                "I am AURA, a Python based personal AI assistant created as a school project."
            )

        return CommandResult(
            "I did not understand that command. Try asking for the time, "
            "opening a website, calculating something, or searching the web."
        )
