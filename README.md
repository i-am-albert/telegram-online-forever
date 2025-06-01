# Telegram Online Forever Bot

This Python script uses the Telethon library to keep your Telegram user account appearing "online." It periodically sends an update status request to Telegram's servers.

**Disclaimer: Using self-bots (automating a regular user account) is against Telegram's Terms of Service. Your account could be flagged or banned. Use this script at your own risk. For most automation tasks, consider using Telegram's official Bot API.**

## What it Does

*   Connects to your Telegram account as a user.
*   Periodically sends a status update to Telegram to indicate "online" presence.
*   Supports authentication via **String Sessions** (recommended for deployment) or file-based sessions (mainly for local testing).
*   Uses environment variables for configuration, keeping your sensitive API credentials and session data out of the codebase.
*   Includes basic error handling and reconnection attempts.

## Features

*   Keeps your Telegram account appearing online.
*   Secure configuration via environment variables.
*   **Primary authentication method for deployment: String Sessions.**
*   Fallback to file-based sessions for local development/testing.
*   Includes an example environment file (`.env.example`).
*   Suitable for deployment on platforms like Railway, Heroku, etc.

## Prerequisites

*   **Python 3.7+**
*   **pip** (Python package installer)
*   **Git** (for cloning the repository)
*   **Telegram API Credentials:**
    *   Go to [https://my.telegram.org/apps](https://my.telegram.org/apps)
    *   Log in with your phone number.
    *   Create a new application (e.g., App title: "MyOnlineBot", Short name: "onlinebot").
    *   You will receive an `api_id` (an integer) and `api_hash` (a string). Keep these safe.

## Setup and Installation (Local)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/telegram-online-forever.git
    cd telegram-online-forever
    ```
    *(Replace `your-username` with your actual GitHub username)*

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    *   Activate the virtual environment:
        *   **Windows (CMD/PowerShell):** `.\venv\Scripts\activate`
        *   **Linux/macOS:** `source venv/bin/activate`

3.  **Install Dependencies:**
    The `requirements.txt` file should contain `telethon` and `python-dotenv`.
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

This script is configured using environment variables. Refer to `.env.example` for all available options.

1.  **Create a `.env` file (for local development):**
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    *(On Windows, you might use `copy .env.example .env`)*

2.  **Edit the `.env` file:**
    Open `.env` and fill in your `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`.
    For local development, you can either:
    *   Leave `TELEGRAM_STRING_SESSION` commented out or empty. The script will then use a file-based session (e.g., `my_account_online_telethon.session`).
    *   Or, generate a string session (see "Generating a String Session" below) and paste it into `TELEGRAM_STRING_SESSION` in your `.env` file.

    **IMPORTANT:** The `.env` file contains sensitive credentials. **Never commit your `.env` file to Git.** Ensure `.env` is listed in your `.gitignore` file.

## Generating a String Session (Recommended for Deployment)

For deploying to platforms like Railway, using a String Session is the easiest and most secure way to authenticate without interactive login.

1.  **Create `generate_session.py`:**
    In your project directory, create a file named `generate_session.py` with the following content:
    ```python
    # generate_session.py
    import os
    from telethon.sync import TelegramClient # Use sync version for simple script
    from telethon.sessions import StringSession

    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("Loaded .env variables for session generation.")
    except ImportError:
        print("python-dotenv not found, ensure API_ID and API_HASH are system env vars or hardcoded.")

    API_ID_STR = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')

    if not API_ID_STR or not API_HASH:
        print("Error: TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env or as environment variables.")
        exit()
    
    API_ID = int(API_ID_STR)

    print("Starting session generation...")
    # Using StringSession() directly and then client.start() will fill it.
    with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        # client.start() will prompt for phone, code, and 2FA if needed.
        # The session string is obtained after successful connection.
        # For more control, you can do manual sign-in:
        print("Please enter your phone number, then the code, and 2FA password if prompted.")
        client.start() # This handles the interactive login prompts

        if client.is_connected() and client.is_user_authorized():
            string_session_data = client.session.save()
            print("\nSuccessfully logged in!")
            print("\nYour String Session is (copy everything below, it's one long line):\n")
            print(string_session_data)
            print("\nStore this string as the TELEGRAM_STRING_SESSION environment variable on your deployment platform (e.g., Railway).")
        else:
            print("\nCould not log in to generate session string.")
    ```

2.  **Ensure `.env` has API_ID and API_HASH:** Make sure your local `.env` file (or system environment variables) contains your `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`.
3.  **Run the Generator:**
    ```bash
    python generate_session.py
    ```
4.  **Follow Prompts:** Enter your phone number, the code Telegram sends you, and your 2FA password (if enabled) in your local terminal.
5.  **Copy the String Session:** After successful login, a long string will be printed. Copy this entire string. This is your `TELEGRAM_STRING_SESSION`.

## Running the Bot Locally

1.  Ensure your virtual environment is activated and you have configured your `.env` file (either for file-based or string-based session).
2.  Run the main script (e.g., `main.py` or `keep_online_telethon_env.py`):
    ```bash
    python main.py
    ```
3.  **First-Time Login (if using file-based session):**
    *   The script will prompt for your phone number, code, and 2FA password.
    *   A `.session` file will be created. On subsequent runs with file-based session, these prompts will be skipped.
    *   **Note:** The server-focused `main.py` will not attempt interactive login if `TELEGRAM_STRING_SESSION` is not set. For initial file-based authentication, you might need a simpler local script or temporarily modify `main.py` to include `input()` calls.

4.  The bot will now run. Press `Ctrl+C` to stop it.

## Deploying to a Platform (e.g., Railway)

1.  **Generate String Session:** Follow the steps above to generate your `TELEGRAM_STRING_SESSION`.
2.  **Push your code to GitHub:** Ensure `.env` is in `.gitignore` and NOT committed.
3.  **Connect your GitHub repository** to Railway (or your chosen platform).
4.  **Set Environment Variables on the Platform:**
    In your platform's dashboard/settings for your application/service, set:
    *   `TELEGRAM_API_ID`: Your API ID
    *   `TELEGRAM_API_HASH`: Your API Hash
    *   `TELEGRAM_STRING_SESSION`: The long string session you generated.
    *   `TELEGRAM_UPDATE_INTERVAL_MINUTES` (Optional, defaults to `5`)
5.  **Deployment:**
    *   The platform will build and deploy your application. Ensure it installs dependencies from `requirements.txt`.
    *   Set the **Start Command** on your platform to run your main script (e.g., `python main.py` or `python keep_online_telethon_env.py`).

## Important Notes

*   **Telegram ToS:** Be aware of the risks of using self-bots.
*   **Credentials Security:** Keep your `API_ID`, `API_HASH`, and especially your `TELEGRAM_STRING_SESSION` extremely secure. Do not share them. If a string session is compromised, generate a new one and update your environment variables. You can also terminate all active sessions via Telegram's settings.
*   **Online Status Nuances:** Telegram's display of "online" status is complex. This script does its best to signal activity.
*   **Error Handling:** The script includes basic error handling. For robust, long-term operation, consider more advanced logging.

## Contributing

Feel free to open issues or pull requests.

## License

This project is open-source. Consider adding a specific license file (e.g., MIT License).