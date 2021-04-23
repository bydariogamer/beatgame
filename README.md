# BEATGAME
This game was born as an entry for the _II Pygame Community Server Game Jam_.
It uses procedural generation of levels... based on music!
Feel free to include your own songs at the `assets/songs` and try to your custom level.

## REQUIREMENTS
Tested on Python 3.9
Requires `numpy` and `pygame` modules, that can be easily installed opening a terminal in the main folder of the game and running:
For compatibility reasons, `pydub` and `ffmpeg` modules might be needed if you want to use other formats than `.ogg` and `.wav`.
All the requirements can be easily installed using:
```pip install -r requirements.txt```
In testing versions we use `matplotlib` to show some statistics.
You can install development requirements using:
```pip install -r requirements-dev.txt```

## LICENSE
The game itself is under the GNU GPL 3.0+ (you can read a copy in [`LICENSE`](LICENSE)), but the songs can have their own license. Check them at [`CREDITS.md`](CREDITS.md).
