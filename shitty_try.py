import telegram
import asyncio
  # Replace with the actual user ID

bot = telegram.Bot(token=bot_token)


async def send_message_to_user(user_id, message):
    try:
        bot_token = '7369046862:AAFZfY9rd0Xrf6K6HDBTs788q8E3hBPV__M'

        await bot.send_message(chat_id=user_id, text=message)
        print("Message sent successfully!")
    except telegram.TelegramError as e:
        print(f"Error sending message: {e}")

async def main():
    message_to_send = "This is a message for you!"
    user_id = 5937741258
    await send_message_to_user(user_id, message_to_send)

asyncio.run(main())
