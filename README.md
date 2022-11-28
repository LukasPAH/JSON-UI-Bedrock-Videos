# JSON-UI-Bedrock-Videos

This branch represents an attempt at implementing support for running via Ubuntu. Might end up with like 5000 commits lol

## What is this?
This repo hosts a Python script to make videos in Minecraft Bedrock JSON UI. This is extremely experimental, and is very only likely to run on high end Windows hardware. It will
crash Minecraft on a phone when run. Sorry not sorry.

## How does it work?
The bulk of the work is carried out by [ffmpeg](https://www.ffmpeg.org/). It splits up the video into individual frames, and converted into readable UI textures.
Do be careful, packs can get extremely big when the individual images are added.
The sound is also split up and added to sound definitions.

## How can I use it?
This script requires [Python 3.10 or greater](https://www.python.org/downloads/) to run. It only runs on Windows, with no other platform support.
For the moment, there are no standalone binaries. You may clone this repo or [download the repo as a zip](https://github.com/LukasPAH/JSON-UI-Bedrock-Videos/archive/refs/heads/main.zip)
and run main.py.

The output resource pack files are very only likely going to run on a beefy Windows machine with Minecraft. Memory usage can exceed 15GB depending on the size of the images
and length of the video.

## Customizable settings (asked in the CLI when run).
### Scene Name
This is the name internally used by your video. You will be able to trigger the video with `/title @p actionbar scene_name` and trigger the sound with `/playsound scene_name:scene_name.play`.
### Video Source
The directory where your input video is. Please wrap in quotes.
### Quality
Two options for image quality: high (.png extension) and low (.jpg extension).
### FPS
The target FPS you want the video to play in-game.

You can then drag the contents in the `output` folder into your resource pack.

## License
As stated earlier, this script heavily utilizes [ffmpeg](https://www.ffmpeg.org/), which is licensed under [GPLv3](COPYING.GPLv3). The files were obtained as part of the "essentials" from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and a mirror of the utilized version can be found [here](https://github.com/GyanD/codexffmpeg/releases/tag/2022-02-14-git-59c647bcf3)