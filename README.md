# Telegram Online Forever Bot

This Python script uses the Telethon library to keep your Telegram user account appearing "online." It periodically sends an update status request to Telegram's servers.

**Disclaimer: Using self-bots (automating a regular user account) is against Telegram's Terms of Service. Your account could be flagged or banned. Use this script at your own risk. For most automation tasks, consider using Telegram's official Bot API.**

## What it Does

*   Connects to your Telegram account as a user.
*   Periodically sends a status update to Telegram to indicate "online" presence.
*   Handles session persistence, so you only need to log in with your phone number and code (and 2FA password if enabled) on the first run.
*   Uses environment variables for configuration, keeping your sensitive API credentials out of the codebase.
*   Includes basic error handling and reconnection attempts.

## Features

*   Keeps your Telegram account appearing online.
*   Secure configuration via environment variables.
*   Session management for easy subsequent runs.
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

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/i-am-albert/telegram-online-forever.git
    cd telegram-online-forever
    ```
    *(Replace `i-am-albert` with your actual GitHub username)*

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    *   Activate the virtual environment:
        *   **Windows (CMD/PowerShell):** `.\venv\Scripts\activate`
        *   **Linux/macOS:** `source venv/bin/activate`

3.  **Install Dependencies:**
    Make sure you have a `requirements.txt` file with at least `telethon` and `python-dotenv`:
    ```
    # requirements.txt
    telethon
    python-dotenv
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

This script is configured using environment variables.

1.  **Create a `.env` file:**
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    *(On Windows, you might use `copy .env.example .env`)*

2.  **Edit the `.env` file:**
    Open the newly created `.env` file and fill in your actual credentials and any desired optional settings:

    ```env
    # .env file

    # --- Required Telegram API Credentials ---
    TELEGRAM_API_ID="YOUR_ACTUAL_API_ID"
    TELEGRAM_API_HASH="YOUR_ACTUAL_API_HASH"

    # --- Optional Configuration ---
    # TELEGRAM_SESSION_NAME="my_custom_session_name"
    # TELEGRAM_UPDATE_INTERVAL_MINUTES="10"
    ```
    *   Replace `YOUR_ACTUAL_API_ID` and `YOUR_ACTUAL_API_HASH` with the values you obtained from Telegram.
    *   `TELEGRAM_SESSION_NAME`: (Optional) The name for the session file (e.g., `my_session.session`). Defaults to `my_account_online_telethon`.
    *   `TELEGRAM_UPDATE_INTERVAL_MINUTES`: (Optional) How often, in minutes, to send the online status update. Defaults to `5`.

    **IMPORTANT:** The `.env` file contains sensitive credentials. **Never commit your `.env` file to Git.** Ensure `.env` is listed in your `.gitignore` file.

## Running the Bot Locally

1.  Make sure your virtual environment is activated and you have configured your `.env` file.
2.  Run the script:
    ```bash
    python keep_online_telethon_env.py
    ```
3.  **First-Time Login:**
    *   The script will prompt for your phone number (e.g., `+1234567890`).
    *   Telegram will send a login code to your account. Enter this code.
    *   If you have Two-Factor Authentication (2FA) enabled, it will ask for your password.
    *   A session file (e.g., `my_account_online_telethon.session`) will be created. On subsequent runs, the script will use this session.

4.  The bot will now run, printing status updates to the console. Press `Ctrl+C` to stop it.

## Deploying to a Platform (e.g., Railway, Heroku)

This script is well-suited for deployment on cloud platforms that support Python and environment variables.

1.  **Push your code to GitHub** (ensure `.env` is in `.gitignore` and NOT committed).
2.  **Connect your GitHub repository** to your chosen platform (e.g., Railway).
3.  **Set Environment Variables on the Platform:**
    Instead of using a `.env` file, you will set the environment variables directly in your platform's dashboard/settings for your application/service:
    *   `TELEGRAM_API_ID`: Your API ID
    *   `TELEGRAM_API_HASH`: Your API Hash
    *   `TELEGRAM_SESSION_NAME` (Optional)
    *   `TELEGRAM_UPDATE_INTERVAL_MINUTES` (Optional)
4.  **Deployment:**
    The platform will typically build and deploy your application. It should automatically install dependencies from `requirements.txt` and run your script (you might need to specify the run command, e.g., `python keep_online_telethon_env.py`, in the platform's settings).
5.  **Session File Persistence:**
    *   Some platforms offer persistent storage, which is ideal for the Telethon `.session` file. If your platform has ephemeral filesystems (files are lost on restart/redeploy), the bot will need to re-authenticate (request phone/code) each time it starts after a full restart.
    *   Railway's persistent volumes can be used for this. You'd configure a volume and map the directory where the session file is stored (the root of your project by default, or a specific path if you modify `SESSION_NAME` to include a directory).

## Important Notes

*   **Telegram ToS:** Again, be aware that using self-bots is against Telegram's Terms of Service and can lead to account restrictions.
*   **API Credentials:** Keep your `API_ID`, `API_HASH`, and `.session` file secure. Do not share them.
*   **Online Status Nuances:** Telegram's display of "online" status to other users is complex. This script performs the most direct action to signal activity, but other factors (network, Telegram's internal logic) can influence it.
*   **Error Handling:** The script includes basic error handling. For robust, long-term operation, you might consider more advanced logging and error management.

## Contributing

Feel free to open issues or pull requests if you have suggestions for improvements or bug fixes.

## License

This project is open-source. You can use and modify it freely, but please be aware of the risks involved with self-bots. Consider adding a specific license file (e.g., MIT License) if you wish.