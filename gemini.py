#!/usr/bin/env python3

import sys

import textwrap
from api_object import ApiObject

from threading import Thread, Event
import time
from yaspin import yaspin

from google.generativeai.types.generation_types import StopCandidateException, BlockedPromptException  # Import the exception class

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# models/chat-bison-001
# models/text-bison-001
# models/embedding-gecko-001
# models/gemini-pro
# models/gemini-pro-vision
# models/embedding-001
# models/aqa

model_name = "gemini-pro"

user_name = "user"

def get_prefix():
    return ("\n(" + user_name + "): ")\

def spinner(stop_event):
    indicators = ['/', '-', '\\', '|']
    while not stop_event.is_set():
        for indicator in indicators:
            print(indicator, end='', flush=True)
            time.sleep(0.11)
            print('\b', end='', flush=True)

def print_help():
    print("command: exit")
    print("         closes program and flushes context\n")
    print("command: print")
    print("         export the conversation history as a text file\n")

apio = ApiObject()

def parse_args():
    if len(sys.argv) < 2:
        return False, ""
    else:
        my_str: str = ""
        for i in range (1, len(sys.argv)):
            my_str += sys.argv[i]
            if i < len(sys.argv) - 1:
                my_str += " "
    return True, my_str

args_exist, first_prompt = parse_args()

while True:

    if args_exist:
        prompt = first_prompt
        args_exist = False
    else:
        prompt = input(get_prefix())

    if prompt in ["help", "-h", "--help"]:
       print_help()
       continue

    if prompt in ["exit", "print", "export"]:
        if prompt != "exit":
            apio.save_chat_history()
            continue
        else:
            break

    stop_event = Event()
    spinner_thread = Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()

    try:
        response = apio.send_message(prompt)
    except StopCandidateException as e:
        pass
        print("Stop candidate exception thrown...")
        # Debug here. Try to extract the response.
        # Extract and print the text from the exception
        response_content = e.args[0].content.parts[0].text
    except BlockedPromptException as e:        
        stop_event.set()
        spinner_thread.join()
        print('\b', end='', flush=True)
        print("Prompt blocked.")
        reason = e.args[0].BlockReason
        continue
    
    stop_event.set()

    spinner_thread.join()

    print("\n("+model_name+"): ")

    if 'response' in locals():
        for chunk in response:
            print("_"*80 + "\n")
            print(chunk.text)
            print("_"*80)

