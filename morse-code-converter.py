"""
Advanced Text ↔ Morse Code Converter (GUI)
Author: Wira

Features:
- Text to Morse conversion
- Morse to Text conversion
- Morse sound playback (beeps)
- Dark mode toggle
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import winsound  # Windows only


# ===================== MORSE DATA =====================

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
}

REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}


# ===================== CONVERSION =====================

def text_to_morse(text):
    result = []
    for char in text.upper():
        if char == " ":
            result.append("/")
        elif char in MORSE_CODE_DICT:
            result.append(MORSE_CODE_DICT[char])
    return " ".join(result)


def morse_to_text(morse):
    result = []
    words = morse.split(" / ")
    for word in words:
        letters = word.split()
        for letter in letters:
            result.append(REVERSE_MORSE_DICT.get(letter, ""))
        result.append(" ")
    return "".join(result).strip()


# ===================== SOUND =====================

def play_morse_sound(morse):
    DOT_DURATION = 150
    DASH_DURATION = 450
    FREQUENCY = 800

    for symbol in morse:
        if symbol == ".":
            winsound.Beep(FREQUENCY, DOT_DURATION)
        elif symbol == "-":
            winsound.Beep(FREQUENCY, DASH_DURATION)
        elif symbol == "/":
            time.sleep(0.5)
        else:
            time.sleep(0.2)


# ===================== GUI =====================

class MorseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Converter")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.dark_mode = False
        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("default")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

        bg = "#1e1e1e" if self.dark_mode else "#f0f0f0"
        fg = "#ffffff" if self.dark_mode else "#000000"

        self.root.configure(bg=bg)

        for widget in self.root.winfo_children():
            try:
                widget.configure(background=bg, foreground=fg)
            except:
                pass

    def create_widgets(self):
        self.title = ttk.Label(
            self.root,
            text="Text ↔ Morse Code Converter",
            font=("Segoe UI", 16, "bold")
        )
        self.title.pack(pady=10)

        self.input_text = tk.Text(self.root, height=6)
        self.input_text.pack(fill="x", padx=20)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Text → Morse", command=self.convert_to_morse).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Morse → Text", command=self.convert_to_text).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Play Beep", command=self.play_sound).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode).grid(row=0, column=3, padx=5)

        self.output_text = tk.Text(self.root, height=6, state="disabled")
        self.output_text.pack(fill="x", padx=20, pady=10)

    def update_output(self, content):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, content)
        self.output_text.config(state="disabled")

    def convert_to_morse(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Error", "Input cannot be empty")
            return
        self.update_output(text_to_morse(text))

    def convert_to_text(self):
        morse = self.input_text.get("1.0", tk.END).strip()
        if not morse:
            messagebox.showwarning("Error", "Input cannot be empty")
            return
        self.update_output(morse_to_text(morse))

    def play_sound(self):
        morse = self.output_text.get("1.0", tk.END).strip()
        if not morse:
            messagebox.showwarning("Error", "Nothing to play")
            return
        play_morse_sound(morse)


# ===================== RUN =====================

def main():
    root = tk.Tk()
    app = MorseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
