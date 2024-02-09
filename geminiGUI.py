#!/usr/bin/env python3

import tkinter as tk
from tkinter import scrolledtext
import threading
import os


from api_object import ApiObject
from text_format import TextFormatter

model_name = "gemini-pro"

def send_message(apio, text_formatter):
    if apio.GEMINI_KEY is None:
        print_no_key_error()
        return

    if apio.GEMINI_KEY is None:
        print_no_key_error()
        return

    while send_button.cget("state") == "disabled":
        pass

    prompt = entry.get("1.0", tk.END).strip()

    if prompt == "":
        return
    
    entry.delete("1.0", tk.END)
    if prompt in ["exit", "print", "export"]:
        if prompt != "exit":
            apio.save_chat_history()
            return
        root.destroy()
        return
    
    update_conversation(text_formatter.query_to_text(prompt))

    root.update()

    def send_message_thru_api():
        response = apio.send_message(prompt)
        root.after(0, lambda: update_conversation(text_formatter.response_to_text(response)))

    thread = threading.Thread(target=send_message_thru_api)
    thread.start()

def update_conversation(response_str: str):
    conversation.config(state='normal')  # Enable editing of the widget
    conversation.insert(tk.END, response_str + "\n")
    conversation.see(tk.END)
    conversation.config(state='disabled')  # Disable editing again


def print_no_key_error():
    update_conversation("No key detected!")
    update_conversation("Use settings to set your API key.")



def print_no_key_error():
    update_conversation("No key detected!")
    update_conversation("Use settings to set your API key.")

    
def open_settings(apio):
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x150")  # Adjust the size as needed

    # Label for the API key entry
    api_key_label = tk.Label(settings_window, text="Enter API Key:")
    api_key_label.pack(pady=(10, 0))  # Add some padding on the y-axis

    # Entry widget for API key
    api_key_entry = tk.Entry(settings_window)
    api_key_entry.pack(pady=(5, 10))  # Add some padding

    # Function to handle the submission of the API key
    def submit_api_key():
        entered_key = api_key_entry.get()
        apio.update_key(entered_key)
        settings_window.destroy()

    # Submit button for the API key
    submit_button = tk.Button(settings_window, text="Submit", command=submit_api_key)
    submit_button.pack()

def on_enter_key(apio, text_formatter):
    send_message(apio, text_formatter)
    return "break"

def insert_newline(event):
    if event.state & 0x4 or event.state & 0x1:  # 0x4 is the mask for the Ctrl key, 0x1 for Shift
        entry.insert(tk.INSERT, "\n")
    return "break"  # Prevents the default newline insertion.

apio = ApiObject()

text_formatter = TextFormatter("user", "gemini-pro")

root = tk.Tk()

if os.name == "nt":
    try:
        root.iconbitmap('GeminiProLogo.ico')
    except tk.TclError as e:
        pass

root.title("Chat with Gemini Pro")

conversation = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
conversation.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=10, fill=tk.X, expand=False)

entry = tk.Text(entry_frame, height=4, wrap=tk.WORD)

entry.bind("<Return>", lambda event: on_enter_key(apio=apio, text_formatter=text_formatter))
entry.bind("<Control-Return>", insert_newline)
entry.bind("<Shift-Return>", insert_newline)

button_frame = tk.Frame(entry_frame)
button_frame.pack(side=tk.RIGHT, padx=5, fill=tk.Y)

send_button = tk.Button(button_frame, text="Send", command=lambda: send_message(apio, text_formatter))
send_button.pack(side=tk.TOP)

settings_button = tk.Button(button_frame, text="Settings", command=lambda: open_settings(apio))
settings_button.pack(side=tk.BOTTOM)

entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

if apio.GEMINI_KEY is None:
    print_no_key_error()
    

root.mainloop()
