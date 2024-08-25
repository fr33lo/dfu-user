from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="discord-file-updater",
    version="0.3.0",
    author="freelo",
    author_email="hi@freelo.club",
    description="A tool to automatically update local files from Discord channels using a user account",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fr33lo/discord-file-updater",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "discord.py>=2.1.0",
        "aiohttp>=3.8.1",
        "python-dotenv>=0.20.0",
    ],
    entry_points={
        "console_scripts": [
            "discord-file-updater=discord_file_updater.main:main",
        ],
    },
    license="MIT",
)