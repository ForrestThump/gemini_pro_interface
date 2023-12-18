Run geminiGUI.py for a Tk GUI interface.

Run gemini.py for a CLI interface.

Get a key from here:
https://ai.google.dev/tutorials/setup

Save your api key as an environment variable assigned to "gemini_key".

If you are using Windows, just enter your API key under settings in the GUI and it will set the environment variable automatically (restarting of GUI required for some reason...).
If you are using Linux, you can enter your API key under settings, but it will not save the key for you.

You can change your model by changing the hard coded '3' number in the ApiObject constructor. I just have it set to Gemini-Pro since it's the one I'm interested in.
