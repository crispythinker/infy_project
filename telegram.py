import telebot

# Credentials
BOT_TOKEN = "5898257753:AAH7h9CyYOJyuoabPJeERJQj5yHSOsJsv88"
CHAT_ID = "5282526140"  # Verified chat ID

bot = telebot.TeleBot(BOT_TOKEN)

# Function to send Telegram message
def send_telegram_message(message):
    try:
        bot.send_message(CHAT_ID, message)
        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send message: {e}")

# # Main function
# def main():
#     message = input("Enter your message: ")
#     if message.strip():
#         send_telegram_message(message)
#     else:
#         print("Message cannot be empty.")

# if __name__ == "__main__":
#     main()
