# generate_session.py
import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Load from .env or set directly
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded .env variables for session generation.")
except ImportError:
    print("python-dotenv not found, ensure API_ID and API_HASH are system env vars or hardcoded for generation.")

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')

if not API_ID or not API_HASH:
    print("Error: TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env or as environment variables.")
    exit()

API_ID = int(API_ID)

print("Starting session generation...")
# Using 'None' as the session name means it won't create a file
# We use 'with' to ensure the client is properly closed
with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("Please enter your phone number, code, and 2FA password if prompted.")
    # The client.start() method will prompt for login if not authorized
    # For string session, it doesn't save to a file but holds in memory.
    # We're not calling client.start() directly like this.
    # Instead, we let the StringSession() do its magic inside the constructor and save_ CallOptions
    # When you run client.connect() and then client.send_code_request etc.
    # it will use the in-memory string session.
    # After successful sign-in, client.session.save() gives the string.

    if not client.is_connected(): # Ensure connected before sign-in flow
        client.connect()

    if not client.is_user_authorized():
        phone = input("Enter phone number: ")
        client.send_code_request(phone)
        client.sign_in(phone, input("Enter code: "))
        # If 2FA is enabled, it will raise SessionPasswordNeededError
        # and you'll have to handle it or it will prompt if using client.start()
        # For manual sign in:
        if not client.is_user_authorized(): # Check again, may need password
            try:
                client.sign_in(password=input("2FA Password (if any, press Enter if none): "))
            except Exception as e:
                print(f"Error during 2FA: {e}")
                exit()
    
    if client.is_user_authorized():
        print("\nSuccessfully logged in!")
        string_session_data = client.session.save()
        print("\nYour String Session is (copy everything below):\n")
        print(string_session_data)
        print("\nStore this string as the TELEGRAM_STRING_SESSION environment variable on Railway.")
    else:
        print("\nCould not log in to generate session string.")