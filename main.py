import os
import shutil
from ffmpeg import ffmpeg

scene = str(input("Scene Name: "))

# Nuke the output directory, if it exists.
if os.path.exists("output"):
    shutil.rmtree("output")

# Re-create output folder.
os.mkdir("output")

# Create a texture folder.
os.mkdir("output/textures")

# Create a sounds folder.
os.mkdir("output/sounds")

# Create our custom content folder.
os.mkdir("output/textures/{scene}".format(scene=scene))

# Run ffmpeg.
ffmpeg(0, "", "L", 30, scene)
