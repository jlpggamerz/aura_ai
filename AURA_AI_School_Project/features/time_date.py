from datetime import datetime

class TimeDate:
    def time(self):
        return "The current time is " + datetime.now().strftime("%I:%M %p") + "."

    def date(self):
        return "Today's date is " + datetime.now().strftime("%d %B %Y") + "."
