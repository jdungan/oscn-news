# OSCN News

A tool for scraping Oklahoma State Courts Network (OSCN) decisions, generating summaries, and creating podcast-ready content from legal news.

## Overview

OSCN News automatically retrieves the latest court decisions from the Oklahoma State Courts Network, processes the data, generates AI-powered summaries, and creates podcast scripts and audio files for legal news distribution.

## Features

- **Data Collection**: Scrapes recent court decisions from the OSCN website
- **AI Summarization**: Uses Mistral-7B to generate concise summaries of complex legal opinions
- **Podcast Generation**: Creates professional podcast scripts that present court decisions in an engaging format
- **Text-to-Speech**: Converts scripts to audio using either Google TTS or ElevenLabs' realistic voices
- **Asynchronous Architecture**: Built with `asyncio` and `aiohttp` for efficient processing

## Requirements

- Python 3.10+
- Poetry for dependency management

## Installation

1. Clone this repository
   ```bash
   git clone https://github.com/jdungan/oscn-news.git
   cd oscn-news
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Create a `.env` file with necessary credentials:
   ```
   OSCN_USER_AGENT="optional_oscn_user_agent"
   ELEVEN_LABS_API_KEY=your_api_key_here
   ```

## Usage

### Data Collection and Processing

The main workflow is implemented in the Jupyter notebook `read_oscn.ipynb`:

1. Fetches recent court decisions from OSCN
2. Parses case details and summaries
3. Generates AI-powered news summaries for each case
4. Creates a podcast script using a language model
5. Converts the script to audio using text-to-speech

### Podcast Publication

For higher quality podcast generation with advanced voice control, use `publish.py`:

```bash
poetry run python publish.py podcast_script_file.txt --output my_podcast.mp3
```

This script:
- Parses a podcast script with voice and sound effect markers
- Generates realistic audio using ElevenLabs voices
- Creates a production-ready podcast file

## Project Structure

- `read_oscn.ipynb`: Jupyter notebook for scraping data and initial processing
- `publish.py`: Script for generating high-quality podcast audio
- `podcasts/`: Directory containing generated podcast audio files
- `poetry.lock` & `pyproject.toml`: Poetry dependency management files

## Models

This project uses the following AI models:
- **Mistral-7B-Instruct-v0.2**: For summarizing court cases and generating podcast scripts
- **ElevenLabs voice models**: For high-quality text-to-speech conversion
- **Google TTS**: Alternative text-to-speech option

## License
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
