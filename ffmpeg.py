import os
import subprocess
import json
from json_assembler import json_assembler

# Run the ffmpeg command.


def run_command(fps, video_file, quality, output):

    # Save the current working directory to memory.
    working_directory = os.getcwd()

    # Change the working directory.
    os.chdir("./ffmpeg/bin")

    # Run ffmpeg, extracting individual frames.
    subprocess.call(
        "ffmpeg.exe -ss 00:00 -i {video_file} -r {fps} \"{dir}\output\\textures\{output}\image-%06d.{quality}\"".format(video_file=video_file, fps=fps, dir=working_directory, output=output, quality=quality))

    # Get audio, first from video to m4a, then from m4a to ogg.
    subprocess.call("ffmpeg.exe -ss 00:00 -i {video_file} -vn -c:a copy \"{dir}\output\\sounds\{output}.m4a\"".format(
        video_file=video_file, output=output, dir=working_directory))
    subprocess.call(
        "ffmpeg.exe -ss 00:00 -i \"{dir}\output\\sounds\{output}.m4a\" -acodec libvorbis -ag 4 -vn -ac 2 -map_metadata 0 \"{dir}\output\\sounds\{output}.ogg\"".format(output=output, dir=working_directory))

    # Remove temp file.
    os.remove("{dir}\output\\sounds\{output}.m4a".format(
        output=output, dir=working_directory))

    # Change the working directory to what it was previously.
    os.chdir(working_directory)

    # Add the sound to the definitions.
    sound_defs = open("output/sounds/sound_definitions.json", "w")
    sound_root = {
        "format_version": "1.14.0",
        "sound_definitions": {
            "{name}:{name}.play".format(name=output): {
                "category": "neutral",
                "sounds": [
                    {
                        "name": "sounds/{name}".format(name=output),
                        "is3D": False,
                        "volume": 1
                    }
                ]
            }
        }
    }
    sound_defs.write(json.dumps(sound_root))
    sound_defs.close()

    # Run the JSON assembler.
    out = output
    json_assembler(out, fps)


# Call ffmpeg.


def ffmpeg(state, file, qual, frames, output_dir):
    # Define starting state and values.
    n = state
    video_file = file
    quality = qual
    fps = frames
    output = output_dir

    if n == 0:
        # User CLI input for video file.
        video_file = input("Video File Location: ")

        # Increment state.
        n = 1

    if n == 1:
        # User CLI input for quality options high=.png, low=.jpeg
        quality = str(
            input("Video Quality (valid options: 'H' or 'L' (high or low)): "))

        # If this is an error, return to top and try again.
        if quality.lower() != "h" and quality.lower() != "l":
            print("Error: valid options are \"H\" or \"L\"")
            ffmpeg(1, video_file, "L", "30", output)

        if quality.lower() == "h" or quality.lower() == "l":
            # Match the case and convert to respective file types.
            match quality:
                case "h":
                    quality = "png"
                case "l":
                    quality = "jpg"

            # Increment state.
            n = 2

    if n == 2:
        # Get the FPS, otherwise throw error if field is wrong.
        try:
            fps = float(str(input("FPS: ")))
            n = 3
        except:
            print("Error: FPS requires int or float!")
            ffmpeg(2, video_file, quality, "30", output)

        # Increment state.

    # Finally, run the ffmpeg commands with the fields above.
    if n == 3:
        run_command(fps, video_file, quality, output)
        return
