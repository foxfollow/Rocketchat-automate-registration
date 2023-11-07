from tokenBot import token as token, chatId
import requests

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = token
chat_id = chatId  # Replace with the chat ID of the user or group you want to send the message to

# URL for the Telegram Bot API
url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

# Message to be sent
message_text = 'Hello, this is a test message from your bot!'

# Parameters for the sendMessage method
params = {
    'chat_id': chat_id,
    'text': message_text,
}

# Send the HTTP POST request to the Telegram Bot API
response = requests.post(url, params=params)

# Print the response from the API (status code and response content)
print(response.status_code, response.text)
