import os
import shutil
from ffmpeg import ffmpeg

scene = str(input("Scene Name: "))

# Nuke the output directory, if it exists.
if os.path.exists("output"):
	shutil.rmtree("output")

# Re-create folders.
os.mkdir("output")
os.mkdir("output/textures")
os.mkdir("output/sounds")
os.mkdir(f"output/textures/{scene}")

# Run ffmpeg.
ffmpeg(0, "", "L", 30, scene)
