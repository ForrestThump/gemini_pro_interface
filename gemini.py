#!/usr/bin/env python3

import pathlib
import textwrap
import os
import datetime

from threading import Thread, Event
import time

import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException  # Import the exception class

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Replace the os.environ["gemini_key"] part with your API key
GEMINI_KEY = os.environ["gemini_key"]

genai.configure(api_key=GEMINI_KEY)

# models/chat-bison-001
# models/text-bison-001
# models/embedding-gecko-001
# models/gemini-pro
# models/gemini-pro-vision
# models/embedding-001
# models/aqa

model_name = "gemini-pro"

model = genai.GenerativeModel(model_name)

chat = model.start_chat(history = [])

def get_prefix():
    return ("\n(" + model_name + "): ")\
    
def spinner(stop_event):
    indicators = ['/', '-', '\\', '|']
    while not stop_event.is_set():
        for indicator in indicators:
            if stop_event.is_set():
                return
            print(indicator, end='', flush=True)
            time.sleep(0.2)
            print('\b', end='')

def save_chat_history(chat):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chat_history_{timestamp}.txt"

    chat_string = ""
    
    for message in chat.history:
        chat_string += f"{message.role}: {message.parts[0].text}\n"

    with open(filename, "a") as text_file:
        text_file.write(chat_string)

def print_help():
    print("command: exit")
    print("         closes program and flushes context\n")
    print("command: print")
    print("         export the conversation history as a text file and closes program\n")

while True:
    prompt = input(get_prefix())

    if prompt == "help":
       print_help()
       continue

    if prompt in ["exit", "print", "export"]:
        if prompt != "exit":
            save_chat_history(chat)
        break

    stop_event = Event()
    spinner_thread = Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()

    try:
        response = chat.send_message(prompt)
    except StopCandidateException as e:
        pass
        # Debug here. Try to extract the response.
        # Extract and print the text from the exception
        response_content = e.args[0].content.parts[0].text
        # print(response_content)
    finally:
        # This will always execute, stopping the spinner and continuing the loop
        stop_event.set()
        spinner_thread.join()

        if 'response' in locals():
            to_markdown(response.text)

            for chunk in response:
                print("_"*80 + "\n")
                print(chunk.text)
                print("_"*80)