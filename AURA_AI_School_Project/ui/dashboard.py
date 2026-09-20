import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime


class AuraDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AURA AI")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

        self.root.configure(bg="#0b0f19")

        # =========================
        # HEADER
        # =========================
        header = tk.Frame(
            self.root,
            bg="#111827",
            height=80
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="A U R A",
            font=("Arial", 26, "bold"),
            fg="#ffffff",
            bg="#111827"
        )
        title.pack(side="left", padx=25)

        subtitle = tk.Label(
            header,
            text="AI PERSONAL ASSISTANT",
            font=("Arial", 10),
            fg="#9ca3af",
            bg="#111827"
        )
        subtitle.pack(side="left", padx=5)

        self.status = tk.Label(
            header,
            text="● ONLINE",
            font=("Arial", 11, "bold"),
            fg="#22c55e",
            bg="#111827"
        )
        self.status.pack(side="right", padx=25)

        # =========================
        # CHAT AREA
        # =========================
        chat_frame = tk.Frame(
            self.root,
            bg="#0b0f19"
        )
        chat_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.chat = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg="#111827",
            fg="#e5e7eb",
            insertbackground="white",
            relief="flat",
            padx=15,
            pady=15
        )

        self.chat.pack(
            fill="both",
            expand=True
        )

        self.chat.insert(
            tk.END,
            "AURA: Hello! I am AURA.\n"
            "AURA: How can I help you today?\n\n"
        )

        self.chat.config(state="disabled")

        # =========================
        # INPUT AREA
        # =========================
        input_frame = tk.Frame(
            self.root,
            bg="#0b0f19"
        )
        input_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.input_box = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bg="#1f2937",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.input_box.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 10)
        )

        self.input_box.bind(
            "<Return>",
            self.send_message
        )

        send_button = tk.Button(
            input_frame,
            text="SEND",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            width=10,
            command=self.send_message
        )

        send_button.pack(
            side="right",
            ipady=8
        )

        # =========================
        # FOOTER
        # =========================
        footer = tk.Frame(
            self.root,
            bg="#111827",
            height=45
        )
        footer.pack(
            fill="x",
            side="bottom"
        )
        footer.pack_propagate(False)

        time_label = tk.Label(
            footer,
            text="AURA AI • Ready",
            font=("Arial", 9),
            fg="#9ca3af",
            bg="#111827"
        )
        time_label.pack(
            side="left",
            padx=20
        )

        exit_button = tk.Button(
            footer,
            text="EXIT",
            command=self.root.destroy,
            font=("Arial", 9, "bold"),
            bg="#374151",
            fg="white",
            relief="flat",
            width=8
        )
        exit_button.pack(
            side="right",
            padx=20
        )

        self.input_box.focus()

    # =========================
    # SEND MESSAGE
    # =========================
    def send_message(self, event=None):

        message = self.input_box.get().strip()

        if not message:
            return

        self.add_message(
            "You",
            message
        )

        self.input_box.delete(
            0,
            tk.END
        )

        response = self.generate_response(message)

        self.add_message(
            "AURA",
            response
        )

    # =========================
    # ADD CHAT MESSAGE
    # =========================
    def add_message(self, sender, message):

        self.chat.config(
            state="normal"
        )

        self.chat.insert(
            tk.END,
            f"{sender}: {message}\n\n"
        )

        self.chat.see(
            tk.END
        )

        self.chat.config(
            state="disabled"
        )

    # =========================
    # BASIC AI RESPONSE
    # =========================
    def generate_response(self, message):

        text = message.lower()

        if text in ["hello", "hi", "hey"]:
            return "Hello! I am AURA. How can I help you?"

        if "time" in text:
            return datetime.now().strftime(
                "The current time is %I:%M %p."
            )

        if "date" in text:
            return datetime.now().strftime(
                "Today's date is %d %B %Y."
            )

        if "who are you" in text:
            return "I am AURA, your personal AI assistant."

        if text in ["exit", "quit"]:
            self.root.after(
                500,
                self.root.destroy
            )
            return "Goodbye!"

        return (
            "I received your message. "
            "My AI brain can be connected here next."
        )

    # =========================
    # RUN
    # =========================
    def run(self):
        self.root.mainloop()