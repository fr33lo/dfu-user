# Discord File Updater (User Client)

Automatically download, manage, and update local files from Discord channels with ease using your personal Discord account.

## Overview

Discord File Updater is a Python script that uses your Discord user account to monitor specified Discord channels (both text and forum) for file attachments, automatically downloads them, and manages versions. It's designed for personal use to keep local files synced with Discord uploads.

## Key Features

- 🖥️ **Multi-Channel Support**: Monitor multiple text and forum channels simultaneously.
- 🔍 **File Type Filtering**: Customize which file types to download based on extensions.
- 📦 **Version Control**: Keep track of file versions with timestamp-based naming.
- 🔔 **Notification System**: Get notified in a specified Discord channel when new files are downloaded.
- 🔒 **Secure**: Uses environment variables for sensitive information.

## Important Note

This script uses a user account token for authentication. Please be aware that using user tokens for automation is against Discord's Terms of Service. This script is intended for personal, non-automated use only. Use it responsibly and at your own risk.

## Technical Details

- Built with Python 3.7+
- Utilizes discord.py for Discord API interaction
- Asynchronous design for efficient performance
- Easy to set up and customize

## Getting Started

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/discord-file-updater.git
   cd discord-file-updater
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   DISCORD_USER_TOKEN=your_user_token_here
   DISCORD_CHANNEL_IDS=channel_id1,channel_id2,channel_id3
   PLUGINS_DIR=/path/to/your/plugins/directory
   ALLOWED_EXTENSIONS=.zip,.jar
   NOTIFICATION_CHANNEL_ID=notification_channel_id
   ```

4. Run the script:
   ```
   python discord_file_updater.py
   ```

## Usage

The script will automatically:
1. Connect to Discord using your user account
2. Check all specified channels for new files
3. Download any new files that match the allowed extensions
4. Send a notification to the specified channel if any files were downloaded
5. Disconnect from Discord

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
