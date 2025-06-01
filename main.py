import asyncio
import getpass
from datetime import datetime
import os
import sys

# Attempt to load environment variables from .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file.")
except ImportError:
    print("python-dotenv not found. Relying on system environment variables.")
    pass # python-dotenv is optional

from telethon import TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.errors import SessionPasswordNeededError

# --- Configuration from Environment Variables ---
# Required:
API_ID_STR = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')

if not API_ID_STR or not API_HASH:
    print("Error: TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables must be set.")
    print("You can set them in your system environment or create a .env file in the script's directory.")
    sys.exit(1)

try:
    API_ID = int(API_ID_STR)
except ValueError:
    print("Error: TELEGRAM_API_ID must be an integer.")
    sys.exit(1)

# Optional with defaults:
DEFAULT_SESSION_NAME = 'my_account_online_telethon'
SESSION_NAME = os.getenv('TELEGRAM_SESSION_NAME', DEFAULT_SESSION_NAME)

DEFAULT_UPDATE_INTERVAL_MINUTES = 5
try:
    UPDATE_INTERVAL_MINUTES = int(os.getenv('TELEGRAM_UPDATE_INTERVAL_MINUTES', DEFAULT_UPDATE_INTERVAL_MINUTES))
    if UPDATE_INTERVAL_MINUTES <= 0:
        print(f"Warning: TELEGRAM_UPDATE_INTERVAL_MINUTES must be a positive integer. Using default: {DEFAULT_UPDATE_INTERVAL_MINUTES} minutes.")
        UPDATE_INTERVAL_MINUTES = DEFAULT_UPDATE_INTERVAL_MINUTES
except ValueError:
    print(f"Warning: TELEGRAM_UPDATE_INTERVAL_MINUTES is not a valid integer. Using default: {DEFAULT_UPDATE_INTERVAL_MINUTES} minutes.")
    UPDATE_INTERVAL_MINUTES = DEFAULT_UPDATE_INTERVAL_MINUTES
# --- End Configuration ---

async def main():
    print("Initializing Telethon Client...")
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    try:
        print("Connecting to Telegram...")
        await client.connect()

        if not await client.is_user_authorized():
            print("First run: Authorization required.")
            phone_number = input("Enter your phone number (e.g., +1234567890): ")
            await client.send_code_request(phone_number)
            try:
                await client.sign_in(phone_number, input('Enter the code you received: '))
            except SessionPasswordNeededError:
                password = getpass.getpass("Two-factor authentication is enabled. Enter your password: ")
                await client.sign_in(password=password)
            except Exception as e:
                print(f"Failed to sign in: {e}")
                return
        else:
            print("Successfully authorized from existing session.")

        me = await client.get_me()
        if me:
            print(f"Logged in as: {me.first_name} (ID: {me.id})")
        else:
            print("Could not get user information. Exiting.")
            return

        print(f"Using session file: {SESSION_NAME}.session")
        print(f"Will send online status updates every {UPDATE_INTERVAL_MINUTES} minutes.")
        print("Press Ctrl+C to stop.")

        while True:
            try:
                if not client.is_connected():
                    print("Client disconnected, attempting to reconnect...")
                    await client.connect()
                    if not await client.is_user_authorized():
                        print("Re-authorization might be needed. Please restart if issues persist.")
                    else:
                        print("Reconnected.")

                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending online status update...")
                await client(UpdateStatusRequest(offline=False))
                await asyncio.sleep(UPDATE_INTERVAL_MINUTES * 60)

            except ConnectionError as e:
                print(f"Connection error: {e}. Attempting to reconnect in 60s...")
                await asyncio.sleep(60)
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Waiting a bit before trying again (60s)...")
                await asyncio.sleep(60)

    except KeyboardInterrupt:
        print("\nStopping self-bot...")
    except Exception as e:
        print(f"A critical error occurred: {e}")
    finally:
        if client.is_connected():
            print("Setting status to offline before disconnecting...")
            try:
                await client(UpdateStatusRequest(offline=True))
            except Exception as e:
                print(f"Could not set offline status: {e}")
            print("Disconnecting client...")
            await client.disconnect()
        print("Client disconnected. Exiting.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting due to user interruption.")