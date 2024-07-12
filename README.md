# IPTV Playlist Generator

This project automates the process of generating IPTV playlists (`playlist.txt` and `main.txt`) by fetching channel data from an IPTV server.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)
- [Contact](#contact)

## Introduction

The IPTV Playlist Generator fetches channel information from an IPTV server and creates two playlists:
- `playlist.txt`: Contains all available channels.
- `main.txt`: Contains selected channels based on provided stream IDs.

## Features

- **Automatic Handshake and Token Retrieval**: Performs a handshake to retrieve the bearer token for authentication.
- **Channel Fetching**: Fetches all channels from the IPTV server.
- **Playlist Generation**: Creates `playlist.txt` with all channels and `main.txt` with selected channels.
- **Scheduled Updates**: Automatically updates the playlists every hour.

## Installation

### Prerequisites

Ensure you have the following installed:

- [Python 3.6+](https://www.python.org/downloads/)

### Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/rajat-ankel/iptv-playlist-generator.git
    cd iptv-playlist-generator
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To start the playlist generation and scheduling, simply run:

```sh
python main.py
