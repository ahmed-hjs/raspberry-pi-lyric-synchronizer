# raspberry-pi-lyric-synchronizer
Raspberry Pi-powered display that shows synchronized song lyrics from LRC files in real time.

## Overview

This project uses a Raspberry Pi to display synchronized song lyrics in real time. Lyrics are loaded from LRC files, which contain timestamps associated with each lyric line.

As the song progresses, the system matches the current playback time with the corresponding lyric timestamps and updates the display automatically.

The project was developed to explore:
- Raspberry Pi development
- File handling and parsing
- Time-based synchronization
- Python programming
- User interface design

## Features

- Real-time lyric display
- Support for standard LRC lyric files
- Automatic lyric synchronization based on timestamps
- Lightweight implementation suitable for Raspberry Pi
- Simple and easy-to-use interface

## Hardware Requirements

- Raspberry Pi
- 16x2 LCD display with I²C backpack (PCF8574)
- Power supply

## Software Requirements

- Python 3

## Project Structure

```text
raspberry-pi-lyric-synchronizer/
│
├── main.py
├── song.lrc
├── README.md
```

## How It Works

1. The user selects an LRC file.
2. The program reads and parses the timestamps and lyric lines.
3. The current playback time is tracked.
4. The program determines which lyric line corresponds to the current timestamp.
5. The display is updated in real time.

## Example LRC File

```text
[00:12.50]Hello darkness my old friend
[00:16.20]I've come to talk with you again
[00:20.80]Because a vision softly creeping
```

Each lyric line is associated with a timestamp in the format:

```text
[minutes:seconds.hundredths]
```

## Demo
### Hardware Setup

<img width="4032" height="3024" alt="IMG_3534 (1)" src="https://github.com/user-attachments/assets/cdfe5520-b8e8-4220-9ba0-b67e0b4165af" />

### Lyric Display



https://github.com/user-attachments/assets/deac5717-9755-48d8-a70c-522d0afcb95b


https://github.com/user-attachments/assets/a49ab185-d59d-4075-93d6-a938d8b360f3



## Challenges Encountered

- Parsing timestamps from LRC files
- Maintaining accurate synchronization between playback time and lyrics
- Designing a display layout that remains readable during updates

## Future Improvements

### Spotify Integration

A future version of the project could integrate with the Spotify Web API to automatically detect the currently playing song and synchronize lyrics without requiring manual file selection.

Potential additions include:

- Automatic song detection
- Playback position synchronization
- Song metadata display
- Album artwork display
- Automatic lyric retrieval

### Additional Features

- Multiple display themes
- Lyric translation
- Wireless song selection
- Touchscreen interface
