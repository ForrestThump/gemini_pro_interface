#!/usr/bin/env python3

import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import datetime

import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException

# Configure your API key and model

try:
    GEMINI_KEY = os.environ["gemini_key"]
except KeyError:
    GEMINI_KEY = None  # or handle it in some other way

genai.configure(api_key=GEMINI_KEY)
model_name = "gemini-pro"
model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

def update_key(input):
    genai.configure(api_key=input)

def send_message():
    prompt = entry.get("1.0", tk.END).strip()
    entry.delete("1.0", tk.END)
    if prompt in ["exit", "print", "export"]:
        if prompt != "exit":
            save_chat_history(chat)
            return
        root.destroy()
        return
    
    loading_label.config(text="Loading...")

    try:
        response = chat.send_message(prompt)
        update_conversation(f"{get_prefix()}{prompt}\n{response.text}")
    except StopCandidateException as e:
        response_content = e.args[0].candidates[0].content.parts[0].text
        update_conversation(f"Exception: {response_content}")
    finally:
        loading_label.config(text="")

def update_conversation(text):
    try:
        conversation.config(state='normal')  # Enable editing of the widget
        conversation.insert(tk.END, text + "\n")
        conversation.see(tk.END)
    except Exception as e:
        print(f"Error updating conversation: {e}")
    finally:
        conversation.config(state='disabled')  # Disable editing again

def open_settings():
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
        update_key(entered_key)

    # Submit button for the API key
    submit_button = tk.Button(settings_window, text="Submit", command=submit_api_key)
    submit_button.pack()



def save_chat_history(chat):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chat_history_{timestamp}.txt"
    with open(filename, "w") as text_file:
        for message in chat.history:
            text_file.write(f"{message.role}: {message.parts[0].text}\n")

def get_prefix():
    return f"({model_name}): "

def on_enter_key(event):
    send_message()
    return "break"

def insert_newline(event):
    if event.state & 0x4 or event.state & 0x1:  # 0x4 is the mask for the Ctrl key, 0x1 for Shift
        entry.insert(tk.INSERT, "\n")
    return "break"  # Prevents the default newline insertion.

root = tk.Tk()
root.title("Chat with Gemini Pro")

conversation = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
conversation.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=10, fill=tk.X, expand=False)

entry = tk.Text(entry_frame, height=4, wrap=tk.WORD)

entry.bind("<Return>", on_enter_key)
entry.bind("<Control-Return>", insert_newline)
entry.bind("<Shift-Return>", insert_newline)

button_frame = tk.Frame(entry_frame)
button_frame.pack(side=tk.RIGHT, padx=5, fill=tk.Y)

send_button = tk.Button(button_frame, text="Send", command=send_message)
send_button.pack(side=tk.TOP)

settings_button = tk.Button(button_frame, text="Settings", command=open_settings)
settings_button.pack(side=tk.BOTTOM)

entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

if GEMINI_KEY is None:
    update_conversation("No key detected!")
    update_conversation("Use settings to set your API key.")

root.mainloop()
