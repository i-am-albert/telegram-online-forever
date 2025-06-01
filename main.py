# main.py (or keep_online_telethon_env.py)
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
    pass
except FileNotFoundError:
    print(".env file not found. Relying on system environment variables.")
    pass

from telethon import TelegramClient
from telethon.sessions import StringSession # Import StringSession
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.errors import SessionPasswordNeededError

# --- Configuration from Environment Variables ---
# Required:
API_ID_STR = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')

if not API_ID_STR or not API_HASH:
    print("Error: TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables must be set.")
    sys.exit(1)

try:
    API_ID = int(API_ID_STR)
except ValueError:
    print("Error: TELEGRAM_API_ID must be an integer.")
    sys.exit(1)

# Session Management:
# Priority to String Session if available, otherwise use file-based session.
STRING_SESSION = os.getenv('TELEGRAM_STRING_SESSION')
DEFAULT_SESSION_NAME = 'my_account_online_telethon' # Used if STRING_SESSION is not set
SESSION_NAME_FILE = os.getenv('TELEGRAM_SESSION_NAME', DEFAULT_SESSION_NAME)


# Optional Behavior Configuration with defaults:
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
    client = None

    if STRING_SESSION:
        print("Found TELEGRAM_STRING_SESSION. Initializing client with StringSession.")
        try:
            client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
        except Exception as e:
            print(f"Error initializing client with StringSession: {e}")
            print("Please ensure the TELEGRAM_STRING_SESSION is valid.")
            sys.exit(1)
    else:
        print(f"No TELEGRAM_STRING_SESSION found. Initializing client with file-based session: {SESSION_NAME_FILE}")
        client = TelegramClient(SESSION_NAME_FILE, API_ID, API_HASH)

    if client is None:
        print("Fatal: Client could not be initialized.")
        sys.exit(1)

    try:
        print("Connecting to Telegram...")
        await client.connect()

        if not await client.is_user_authorized():
            # This block is for file-based sessions or if string session is invalid/expired
            # It should ideally NOT run on a server environment if STRING_SESSION is correctly set.
            if STRING_SESSION:
                print("Error: Not authorized. The provided TELEGRAM_STRING_SESSION might be invalid or expired.")
                print("Please generate a new string session locally and update the environment variable.")
                return # Exit if string session auth fails
            else:
                # Interactive login for file-based session (local development)
                print("Authorization required (file-based session or first run).")
                print("This script is intended for non-interactive environments when TELEGRAM_STRING_SESSION is set.")
                print("If running on a server, ensure TELEGRAM_STRING_SESSION is correctly configured.")
                # Attempting interactive login is likely to fail in non-interactive environments.
                # We will not include the input() calls here for server safety.
                # If you need to run this locally and authenticate for the first time with a file session,
                # you'd re-add the input() based login flow here.
                print("Cannot proceed with interactive login in this environment. Please authenticate locally first if using file session, or use String Session.")
                return

        print("Successfully authorized.")
        me = await client.get_me()
        if me:
            print(f"Logged in as: {me.first_name} (ID: {me.id})")
        else:
            print("Could not get user information. Exiting.")
            return

        if STRING_SESSION:
            print("Using String Session for authentication.")
        else:
            print(f"Using session file: {client.session.filename}")
        print(f"Will send online status updates every {UPDATE_INTERVAL_MINUTES} minutes.")
        print("Press Ctrl+C to stop (if running locally).")

        while True:
            try:
                if not client.is_connected():
                    print("Client disconnected, attempting to reconnect...")
                    await client.connect()
                    if not await client.is_user_authorized():
                        print("Re-authorization failed after reconnect. String session might be invalid.")
                        return # Stop if re-auth fails
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
                # Check if it's an auth error that might indicate expired string session
                if "AUTH_KEY_UNREGISTERED" in str(e).upper() or "SESSION_REVOKED" in str(e).upper():
                    print("Authentication error detected. The session (string or file) may be revoked or expired.")
                    print("Please generate a new session.")
                    return # Stop the bot
                print("Waiting a bit before trying again (60s)...")
                await asyncio.sleep(60)

    except KeyboardInterrupt:
        print("\nStopping self-bot...")
    except Exception as e:
        print(f"A critical error occurred: {e}")
    finally:
        if client and client.is_connected(): # Check if client exists and is connected
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
        print("\nExiting due to user interruption (Ctrl+C).")
    except SystemExit:
        print("Exiting due to internal sys.exit().")
    except Exception as e:
        print(f"Unhandled exception at top level: {e}")