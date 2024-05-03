# Squeak

Squeak is a terminal-based music player for SoundCloud playlists and songs. It's designed to provide a straightforward way to listen to your favorite SoundCloud tracks directly from the command line.

## Features

- Plays SoundCloud playlists and individual songs.
- Simple, direct interface using curses.
- Easy to use: just execute the Python file with the playlist or song links as arguments.

## Requirements

- Python 3.x
- See `requirements.txt` for Python package dependencies.

## Usage

1. Clone this repository:
```bash
git clone https://github.com/SrKlono/squeak.git
```

2. Navigate to the project directory:
```bash
cd squeak
```

3. Execute the main Python file with the SoundCloud playlists or song links as arguments:
```bash
python squeak.py <link1> <link2> <link3>...
```
Replace `<linkX>` with the URLs of the SoundCloud playlists or songs you want to play.

4. Wait for the playlist to load, use the arrow keys to navigate through the playlist and space to pause/unpause the current song. Press `q` to quit.

## Example

Playing a public SoundCloud playlist:
```bash
python squeak.py https://soundcloud.com/missy-mcinerney-266523249/sets/eve
```