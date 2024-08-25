"""
Discord File Updater (User Client)

A tool to automatically update local files from Discord channels using a user account.
"""

# Version of the discord-file-updater package
__version__ = "0.3.0"

# Import main classes/functions to make them easily accessible
from .discord_file_updater import main

# Define what should be imported with "from discord_file_updater import *"
__all__ = ['main']