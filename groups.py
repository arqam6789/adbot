import os
from telethon import TelegramClient
import time

# File to store API credentials
CREDITS_FILE = 'credits.txt'

def get_api_credentials():
    """Get API credentials from the user and save them to a file."""
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API Hash: ")
    
    # Save to credits.txt
    with open(CREDITS_FILE, 'w') as file:
        file.write(f"{api_id}\n{api_hash}\n")
    
    return api_id, api_hash

def load_api_credentials():
    """Load API credentials from the file."""
    if os.path.exists(CREDITS_FILE):
        with open(CREDITS_FILE, 'r') as file:
            lines = file.read().splitlines()
            if len(lines) == 2:
                return lines[0], lines[1]
    return None, None

# Load API credentials or prompt user if not available
api_id, api_hash = load_api_credentials()
if not api_id or not api_hash:
    api_id, api_hash = get_api_credentials()

# Initialize the Telegram client
client = TelegramClient('session_name', int(api_id), api_hash)

async def main():
    await client.start()
    
    # Get the latest message from @talentedtradehub
    channel = await client.get_entity('@ECLIPWZE_HUB')
    messages = await client.get_messages(channel, limit=1)
    
    if not messages:
        print("No messages found in @CLIPWZE_HUB.")
        return
    
    last_message = messages[-1]
    
    # Get all dialogs (conversations)
    dialogs = await client.get_dialogs()
    
    # Filter groups only
    groups = [dialog for dialog in dialogs if dialog.is_group]
    
    # Forward the message to each group with a delay
    for group in groups:
        try:
            await client.forward_messages(group.id, last_message)
            print(f"Message forwarded to {group.name} ({group.id})")
        except Exception as e:
            # Print only the successful forwards, ignore errors like TOPIC_CLOSED
            if "TOPIC_CLOSED" not in str(e):
                print(f"Failed to forward message to {group.name} ({group.id}): {e}")
        time.sleep(2)  # Sleep for 2 seconds before sending to the next group

# Run the client
with client:
    client.loop.run_until_complete(main())
