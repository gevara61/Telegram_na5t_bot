import random
import string
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
from keep_alive import keep_alive  # Import keep_alive

# Start the keep-alive function to keep the bot running on Replit
keep_alive()

# Your user ID (replace with your actual Telegram user ID)
YOUR_USER_ID = 5592595227  # Replace with your actual Telegram user ID

# Global flag to control if the bot should keep generating usernames
should_generate = False

# Generate a random Instagram username
def generate_username():
    # Include letters, digits, dots, and underscores
    characters = string.ascii_lowercase + string.digits + "._"
    username = ''.join(random.choice(characters) for _ in range(4))  # Adjust length as needed
    return username

# Check Instagram username availability (mockup)
def check_username_availability(username: str) -> bool:
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)

    # Instagram returns 404 if the username is available
    return response.status_code == 404

# Function to generate and send the username every X seconds
async def generate_and_send():
    global should_generate
    bot = Bot(token="7614179504:AAFNTFsAFBdQATV7tiTuAly55yNLycbAWmw")

    while should_generate:
        # Generate a random username
        username = generate_username()
        # Check if the username is available on Instagram
        is_available = check_username_availability(username)

        # Prepare the message to send to your Telegram DM
        message = f"Generated Username: {username}\n"
        message += "Availability: " + ("Available" if is_available else "Taken")

        try:
            # Send the result to your Telegram DM
            await bot.send_message(chat_id=YOUR_USER_ID, text=message)
        except Exception as e:
            print(f"Error sending message: {e}")

        # Stop generating if an available username is found
        if is_available:
            should_generate = False
            await bot.send_message(chat_id=YOUR_USER_ID, text=f"Found an available username: {username}! Stopping the process.")
            break

        # Wait for 1 second before generating the next username (adjustable interval)
        await asyncio.sleep(0.1)

# Command to start generating usernames
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global should_generate
    if not should_generate:
        should_generate = True
        # Start the periodic generation task
        asyncio.create_task(generate_and_send())
        await update.message.reply_text("Started generating usernames and sending to your DM!")
    else:
        await update.message.reply_text("The bot is already generating usernames.")

# Command to stop generating usernames
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global should_generate
    if should_generate:
        should_generate = False
        await update.message.reply_text("Stopped generating usernames.")
    else:
        await update.message.reply_text("The bot is not currently generating usernames.")

# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the Instagram username generator bot!")

# Main function to start the bot
def main():
    # Replace 'YOUR_TOKEN_HERE' with your bot's token
    token = "7614179504:AAFNTFsAFBdQATV7tiTuAly55yNLycbAWmw"
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))  # Changed /go to /generate for consistency
    application.add_handler(CommandHandler("stop", stop))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
