from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pyttsx3  # Text-to-speech library
import serial
import speech_recognition as sr  # Voice recognition
import threading 
import time
from esp_down import init_esp_down,esp_down,close_esp_down
from esp_up import init_esp_up,esp_up,close_esp_up

from firebase import read_datahum,read_dataiot,read_dataiot1,read_dataiot2,read_dataiot3,read_dataiot4,read_dataiot5,read_datamoi,read_datatem
from firebase import update_a1,update_a2,update_a3,update_a4,update_a5


from ip import get_local_ipv4
from mail import send_email_to_contact
from remember import set_reminder,get_reminder,get_all_reminders
from telegram import send_telegram_message
from time1 import get_time,get_date,wish_time_of_day
from whatsapp import send_msg
from wikipedia import *

# Use device (CUDA if available, else CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class IntegratedChatbot:
    def __init__(self):
        # Load chatbot model
        self.dialogpt_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium").to(device)
        self.dialogpt_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.chat_history_ids = None  # For conversational history
        print("Models and tokenizers loaded successfully.")

        # Initialize pyttsx3 for text-to-speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

        # Initialize Serial Communication
        self.uart = self.initialize_serial()

    def initialize_serial(self):
        """Initialize UART serial communication."""
        try:
            uart = serial.Serial('/dev/cu.usbserial-58290574931', 115200, timeout=1)
            time.sleep(2)  # Allow time for connection
            print("Serial connection established.")
            return uart
        except serial.SerialException as e:
            print(f"Error initializing serial communication: {e}")
            return None  # Handle case where UART fails

 # To handle stop command timing

    def send_command(self, command):
        """Send movement command to the microcontroller via UART and stop after 3 seconds."""
        if self.uart:
            try:
                self.uart.write(f"{command}\n".encode())  # Send command
                print(f"Sent: {command}")

                # Start a separate thread to send "stop" after 3 seconds
                stop_thread = threading.Thread(target=self.delayed_stop, args=(3,))
                stop_thread.start()

            except serial.SerialException as e:
                print(f"Error sending command: {e}")

    def delayed_stop(self, delay):
        """Wait for `delay` seconds and then send stop command."""
        time.sleep(delay)  # Wait before stopping
        if self.uart:
            try:
                self.uart.write("S\n".encode())  # Send stop command
                print("Sent: Stop (S)")
            except serial.SerialException as e:
                print(f"Error sending stop command: {e}")


    def generate_response(self, user_input):
        """Generate a chatbot response using DialoGPT."""
        new_user_input_ids = self.dialogpt_tokenizer.encode(
            user_input + self.dialogpt_tokenizer.eos_token, return_tensors="pt"
        ).to(device)

        bot_input_ids = torch.cat([self.chat_history_ids[:, -50:], new_user_input_ids], dim=-1) \
            if self.chat_history_ids is not None else new_user_input_ids

        chat_history_ids = self.dialogpt_model.generate(
            bot_input_ids,
            max_length=200,
            pad_token_id=self.dialogpt_tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            no_repeat_ngram_size=2,
        )
        
        self.chat_history_ids = chat_history_ids
        response = self.dialogpt_tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                                                  skip_special_tokens=True)
        return response.strip()

    def speak(self, text):
        """Convert text to speech."""
        self.engine.say(text)
        self.engine.runAndWait()



    def process_command(self, user_input):
        """Process user commands related to movement."""
        command_map = {
            "left": "L",
            "right": "R",
            "forward": "F",
            "backward": "B",
            "stop": "S",
            "battery": "b",
            "full speed": "q",
            "speed 1": "1",
            "speed 2": "2",
            "speed 3": "3",
            "speed 4": "4",
            "speed 5": "5",
            "speed 6": "6",
            "speed 7": "7",
            "speed 8": "8",
            "speed 9": "9",
            "night light off": "n",
            "night light on": "N",
            "daylight off": "w",
            "daylight on": "W"
        }

        for key, value in command_map.items():
            if key in user_input.lower():
                self.send_command(value)
                return f"'{key}'."

        return None  # If no command matches, return None

    def listen(self):
        """Listen for user input via microphone and return text."""
        with self.mic as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust to environment noise
            try:
                audio = self.recognizer.listen(source)
                user_input = self.recognizer.recognize_google(audio)  # Convert speech to text
                print(f"You said: {user_input}")
                return user_input.lower()  # Convert to lowercase for easier processing
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
                return None
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
                return None

    def chat(self):
        """Main chat loop with voice input."""
        print("Chatbot: Hi! How can I help you today?")
        self.speak("Hi! How can I help you today?")
        while True:
            user_input = self.listen()
            # user_input = input("Enter Input: ")
            if not user_input:
                continue  # If no input was detected, restart loop

            if user_input in ["exit", "quit", "bye"]:
                print("Chatbot: Goodbye! Take care!")
                self.speak("Goodbye! Take care!")
                break

            # Check if it's a movement command
            command_response = self.process_command(user_input)
            if command_response:
                print(f"Chatbot: {command_response}")
                self.speak(command_response)
                continue  # Skip chatbot response if a command was executed

            # Handle web search
            if user_input.startswith("search"):
                query = user_input.replace("search", "").strip()
                print(f"Chatbot: Searching for '{query}'...")
                self.speak(f"Searching for {query}...")
                self.handle_web_search(query)
                continue

            # Generate chatbot response
            bot_response = self.generate_response(user_input)
            print(f"Chatbot: {bot_response}")
            self.speak(bot_response)

if __name__ == '__main__':
    bot = IntegratedChatbot()
    bot.chat()
