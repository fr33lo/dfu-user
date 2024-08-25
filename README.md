Discord File Updater (User Client)
Automatically download and manage files from Discord channels with ease using your personal Discord account.
Overview
Discord File Updater is a Python script that uses your Discord user account to monitor specified Discord channels (both text and forum) for file attachments, automatically downloads them, and manages versions. It's designed for personal use to keep local files synced with Discord uploads.
Key Features

🖥️ Multi-Channel Support: Monitor multiple text and forum channels simultaneously.
🔍 File Type Filtering: Customize which file types to download based on extensions.
📦 Version Control: Keep track of file versions with timestamp-based naming.
🔔 Notification System: Get notified in a specified Discord channel when new files are downloaded.
🔒 Secure: Uses environment variables for sensitive information.

Important Note
This script uses a user account token for authentication. Please be aware that using user tokens for automation is against Discord's Terms of Service. This script is intended for personal, non-automated use only. Use it responsibly and at your own risk.
Technical Details

Built with Python 3.7+
Utilizes discord.py for Discord API interaction
Asynchronous design for efficient performance
Easy to set up and customize

Getting Started

Clone this repository:
Copygit clone https://github.com/yourusername/discord-file-updater.git
cd discord-file-updater

Install the required dependencies:
Copypip install -r requirements.txt

Set up your environment variables in a .env file:
CopyDISCORD_USER_TOKEN=your_user_token_here
DISCORD_CHANNEL_IDS=channel_id1,channel_id2,channel_id3
PLUGINS_DIR=/path/to/your/plugins/directory
ALLOWED_EXTENSIONS=.zip,.jar
NOTIFICATION_CHANNEL_ID=notification_channel_id

Run the script:
Copypython discord_file_updater.py


Usage
The script will automatically:

Connect to Discord using your user account
Check all specified channels for new files
Download any new files that match the allowed extensions
Send a notification to the specified channel if any files were downloaded
Disconnect from Discord

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.