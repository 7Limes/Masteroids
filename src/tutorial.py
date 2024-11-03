import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
from globals import ASSETS_PATH

tutorial_open = False


def tutorial_window_loop():
    root = tk.Tk()
    root.title('How to Play')
    with open(f'{ASSETS_PATH}/tutorial.txt', 'r') as f:
        tutorial_text = f.read()
    text_area = ScrolledText(root)
    text_area.insert(tk.INSERT, tutorial_text)
    text_area.configure(state=tk.DISABLED)
    text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    root.mainloop()
    global tutorial_open
    tutorial_open = False


def open_tutorial_window():
    global tutorial_open
    if not tutorial_open:
        tutorial_open = True
        t = threading.Thread(target=tutorial_window_loop)
        t.start()