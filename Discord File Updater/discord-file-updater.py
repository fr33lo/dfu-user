import discord
import aiohttp
import os
import logging
from datetime import datetime
from typing import Optional, Union, Tuple, List
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Setup logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'discord_file_updater.log')
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s', filename=LOG_FILE)
logger = logging.getLogger(__name__)

# Load configuration from environment variables
TOKEN = os.getenv('DISCORD_USER_TOKEN')
CHANNEL_IDS = list(map(int, os.getenv('DISCORD_CHANNEL_IDS', '').split(',')))
PLUGINS_DIR = os.getenv('PLUGINS_DIR', r'C:\Plugins')
ALLOWED_EXTENSIONS = tuple(os.getenv('ALLOWED_EXTENSIONS', '.zip,.jar').split(','))
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 3600))  # Default to 1 hour
NOTIFICATION_CHANNEL_ID = int(os.getenv('NOTIFICATION_CHANNEL_ID', 0))
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 100))
CHECK_ARCHIVED_THREADS = os.getenv('CHECK_ARCHIVED_THREADS', 'true').lower() == 'true'
MAX_CONCURRENT_DOWNLOADS = int(os.getenv('MAX_CONCURRENT_DOWNLOADS', 5))
HISTORY_LIMIT = int(os.getenv('HISTORY_LIMIT', 100))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

download_semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

async def download_file(url: str, filename: str) -> Optional[str]:
    async with download_semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    content_length = int(resp.headers.get('Content-Length', 0))
                    if content_length > MAX_FILE_SIZE_MB * 1024 * 1024:
                        logger.warning(f"File {filename} exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB")
                        return None
                    timestamp = int(datetime.now().timestamp())
                    versioned_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
                    filepath = os.path.join(PLUGINS_DIR, versioned_filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, 'wb') as f:
                        f.write(await resp.read())
                    logger.info(f"File {versioned_filename} downloaded and saved to {filepath}")
                    return versioned_filename
                else:
                    logger.error(f"Failed to download {filename}. Status code: {resp.status}")
                    return None

async def process_message(message: discord.Message) -> Tuple[Optional[discord.Attachment], datetime]:
    if any(attachment.filename.endswith(ALLOWED_EXTENSIONS) for attachment in message.attachments):
        return max(
            (attachment for attachment in message.attachments if attachment.filename.endswith(ALLOWED_EXTENSIONS)),
            key=lambda a: a.created_at
        ), message.created_at
    return None, message.created_at

async def update_channel(channel: Union[discord.TextChannel, discord.ForumChannel]) -> List[str]:
    downloaded_files = []
    try:
        if isinstance(channel, discord.ForumChannel):
            async for thread in channel.archived_threads(limit=None):
                if not CHECK_ARCHIVED_THREADS and thread.archived:
                    continue
                async for message in thread.history(limit=HISTORY_LIMIT):
                    file, _ = await process_message(message)
                    if file:
                        downloaded = await download_file(file.url, file.filename)
                        if downloaded:
                            downloaded_files.append(downloaded)
        elif isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=HISTORY_LIMIT):
                file, _ = await process_message(message)
                if file:
                    downloaded = await download_file(file.url, file.filename)
                    if downloaded:
                        downloaded_files.append(downloaded)

        if not downloaded_files:
            logger.warning(f"No files found in channel {channel.name}")
        return downloaded_files
    except discord.errors.Forbidden:
        logger.error(f"User doesn't have permission to access the channel {channel.name}")
    except Exception as e:
        logger.error(f"An error occurred while updating channel {channel.name}: {str(e)}")
    return []

async def update_all_channels() -> None:
    for channel_id in CHANNEL_IDS:
        channel = client.get_channel(channel_id)
        if channel:
            downloaded_files = await update_channel(channel)
            for file in downloaded_files:
                await send_notification(f"New file downloaded from {channel.name}: {file}")
        else:
            logger.error(f"Channel with ID {channel_id} not found.")

async def send_notification(message: str) -> None:
    if NOTIFICATION_CHANNEL_ID:
        channel = client.get_channel(NOTIFICATION_CHANNEL_ID)
        if channel:
            await channel.send(message)
        else:
            logger.error(f"Notification channel with ID {NOTIFICATION_CHANNEL_ID} not found.")

@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}')
    await update_all_channels()
    await client.close()

def main() -> None:
    if not all([TOKEN, CHANNEL_IDS, PLUGINS_DIR]):
        logger.error("Missing required environment variables. Please set DISCORD_USER_TOKEN, DISCORD_CHANNEL_IDS, and PLUGINS_DIR.")
    else:
        client.run(TOKEN)

if __name__ == "__main__":
    main()
