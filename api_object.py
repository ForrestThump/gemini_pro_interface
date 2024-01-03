
import google.generativeai as genai
import os
import datetime

from google.generativeai.types.generation_types import StopCandidateException, BlockedPromptException  # Import the exception class

class ApiObject:
    def __init__(self) -> None:

        try:
            self.GEMINI_KEY = os.environ["gemini_key"]
        except KeyError:
            self.GEMINI_KEY = None

        genai.configure(api_key=self.GEMINI_KEY)
        
        self.model_names = ["chat-bison-001", 
                            "text-bison-001",
                            "embedding-gecko-001",
                            "gemini-pro",
                            "gemini-pro-vision",
                            "embedding-001",
                            "aqa"]
        
        self.model_name = self.model_names[3]
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat(history = [])

    def send_message(self, query):
        return self.chat.send_message(query, safety_settings=[
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            ])

    def save_chat_history(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_history_{timestamp}.txt"

        chat_string = ""
        
        for message in self.chat.history:
            chat_string += f"{message.role}: {message.parts[0].text}\n"

        with open(filename, "a") as text_file:
            text_file.write(chat_string)

        print("Chat saved in file: " + filename + "\n")

    def refresh_history(self):
        self.chat = self.model.start_chat(history = [])

    def update_key(self, input):
        genai.configure(api_key=input)

        if os.name == "nt": 
            subprocess.run(['setx', 'gemini_key', input], check=True)
