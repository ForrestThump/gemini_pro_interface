import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import datetime

import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException

# Configure your API key and model
GEMINI_KEY = os.environ["gemini_key"]
genai.configure(api_key=GEMINI_KEY)
model_name = "gemini-pro"
model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

def send_message():
    prompt = entry.get()
    if prompt in ["exit", "print", "export"]:
        if prompt != "exit":
            save_chat_history(chat)
        root.destroy()
        return

    try:
        response = chat.send_message(prompt)
        update_conversation(f"{get_prefix()}{prompt}\n{response.text}")
    except StopCandidateException as e:
        response_content = e.args[0].candidates[0].content.parts[0].text
        update_conversation(f"Exception: {response_content}")
    entry.delete(0, tk.END)

def update_conversation(text):
    conversation.insert(tk.END, text + "\n")
    conversation.see(tk.END)

def save_chat_history(chat):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chat_history_{timestamp}.txt"
    with open(filename, "w") as text_file:
        for message in chat.history:
            text_file.write(f"{message.role}: {message.parts[0].text}\n")

def get_prefix():
    return f"({model_name}): "

root = tk.Tk()
root.title("Chat with AI")

conversation = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
conversation.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=10, fill=tk.X, expand=False)

entry = tk.Entry(entry_frame)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

send_button = tk.Button(entry_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

root.mainloop()
