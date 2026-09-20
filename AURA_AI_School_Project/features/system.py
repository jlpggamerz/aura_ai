import os
import platform
import subprocess

class SystemTools:
    def open_calculator(self):
        system = platform.system()
        if system == "Windows":
            subprocess.Popen("calc.exe")
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Calculator"])
        else:
            subprocess.Popen(["gnome-calculator"])

    def open_notepad(self):
        system = platform.system()
        if system == "Windows":
            subprocess.Popen(["notepad.exe"])
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "TextEdit"])
        else:
            subprocess.Popen(["gedit"])

    def open_path(self, path):
        if os.path.exists(path):
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
