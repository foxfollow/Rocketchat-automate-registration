# Import the required modules
import telebot  # A simple and easy-to-use library for Telegram Bot API
import requests  # A library for sending HTTP requests

# Define the bot token
from tokenBot import token as bot_token

# Define the base URL for the Telegram Bot API
base_url = f"https://api.telegram.org/bot{bot_token}/"


# Define a function to get updates from the bot
def get_updates():
    # Send a get request to the getUpdates method
    response = requests.get(base_url + "getUpdates")
    # Check if the response is successful
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()
        # Return the result list
        return data["result"]
    else:
        # Raise an exception if the response is not successful
        raise Exception(f"Failed to get updates: {response.text}")


# Define a function to get a list of all channels and chats where the bot is
def get_channels_and_chats():
    # Initialize an empty dictionary to store the chat names and types
    chats = {}
    # Get the updates from the bot
    updates = get_updates()
    # Loop through the updates
    for update in updates:
        # Check if the update has a message
        if "message" in update:
            # Get the message object
            message = update["message"]
            # Check if the message has a chat
            if "chat" in message:
                # Get the chat object
                chat = message["chat"]
                # Get the chat name and type
                chat_name = chat["title"] if "title" in chat else chat["first_name"]
                chat_type = chat["id"]
                # Add the chat name and type to the dictionary if not already present
                if chat_name not in chats:
                    chats[chat_name] = chat_type
    # Return the dictionary of chat names and types
    return chats


def get_channels():
    # Initialize an empty list to store the channel names
    channels = []
    # Get the updates from the bot
    updates = get_updates()
    # Loop through the updates
    for update in updates:
        # Check if the update has a message
        if "message" in update:
            # Get the message object
            message = update["message"]
            # Check if the message is from a channel
            if "chat" in message and message["chat"]["type"] == "channel":
                # Get the channel name
                channel = message["chat"]["title"]
                # Add the channel name to the list if not already present
                if channel not in channels:
                    channels.append(channel)
    # Return the list of channel names
    return channels


# Print the list of channels and chats where the bot is
print(get_channels_and_chats())
print(get_channels())
