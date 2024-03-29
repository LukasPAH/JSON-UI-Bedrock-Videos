import os
import json
import glob


def json_assembler(scene, fps):

    # Create a UI folder for UI files.
    os.mkdir("output/ui")

    # Write to the hud_screen JSON.
    hud_screen = open("output/ui/hud_screen.json", "w")

    # Define root panel with modification.
    root_panel = {
        "root_panel": {
            "modifications": [
                {
                    "array_name": "controls",
                    "operation": "insert_front",
                    "value": {"{custom_panel}_video_factory@{custom_panel}.{custom_panel}_video_factory".format(custom_panel=scene): {}}
                }
            ]
        }
    }

    # Add property so HUD is rendered below everything.
    hud_tweak = {
        "hud_screen": {
            "render_only_when_topmost": False,
            "$screen_animations": []
        }
    }
    root_panel.update(hud_tweak)

    # Write all the contents to the hud screen.
    hud_screen.write(json.dumps(root_panel))
    hud_screen.close()

    # Open custom namespace.
    custom_file = open("output/ui/{namespace}.json".format(namespace=scene),
                       "w")

    # Define namespace.
    namespace = scene

    # Define the root.
    custom_root = {
        "namespace": "{namespace}".format(namespace=namespace)}

    # Define the image template.
    image_template = {
        "image_template": {
            "type": "image",
            "alpha": 0,
            "ignored": "(not ($corrected_actionbar_text = '{name}'))".format(name=namespace)
        }
    }

    # Define the custom content panel.
    content_panel = {
        "{custom_panel}_content_panel".format(custom_panel=namespace): {
            "type": "panel",
            "layer": 1005,
            "$corrected_actionbar_text": "$actionbar_text",
            "controls": []
        }
    }

    # Get the items in the custom video content directory.

    # Save working directory to memory.
    working_directory = os.getcwd()

    # Change working directory.
    os.chdir(
        "./output/textures/{custom_folder}".format(custom_folder=namespace))

    # Get images.
    images = glob.glob("./*.png")
    jpgs = glob.glob("./*.jpg")
    images.extend(jpgs)

    # Revert working directory.
    os.chdir(working_directory)

    # Duration of animations for rendering frame..
    duration = 0

    # Define n.
    n = 0

    # Iterate through list and add to content panel.
    for items in images:

        # Chop of the unneeded file extension from the item.
        items = items.replace(".\\", "")
        items = items.replace(".png", "")
        items = items.replace(".jpg", "")

        # Define video frame.
        video_frame = {
            "video_frame_{frame_number}@{namespace}.image_template".format(frame_number=items, namespace=namespace): {
                "texture": "textures/{namespace}/{frame_number}".format(namespace=namespace, frame_number=items),
                "anims": ["@{namespace}.{item}_anim".format(namespace=namespace, item=items)],
                "layer": n
            }
        }

        n = n + 1

        # Add video frame to content panel.
        content_panel["{custom_panel}_content_panel".format(
            custom_panel=namespace)]["controls"].append(video_frame)

        # Add duration for waiting anims
        duration = float(1 / fps) + duration

        # Define animation for rendering frame.
        animation = {
            "{item}_anim".format(item=items): {
                "anim_type": "wait",
                "duration": duration,
                "next": "@{namespace}.alpha_in".format(namespace=namespace)
            }
        }

        # Merge the image anims into the root.
        custom_root.update(animation)

    # Define frame time (2.2 to prevent clipping of images).
    frames = 2.2 * float(1 / fps)

    # Other common animations.
    alpha_in = {
        "alpha_in": {
            "anim_type": "alpha",
            "duration": 0,
            "from": 0,
            "to": 1,
            "next": "@{namespace}.alpha_wait".format(namespace=namespace)
        }
    }
    custom_root.update(alpha_in)

    alpha_wait = {
        "alpha_wait": {
            "anim_type": "wait",
            "duration": frames,
            "next": "@{namespace}.alpha_out".format(namespace=namespace)
        }
    }
    custom_root.update(alpha_wait)

    alpha_out = {
        "alpha_out": {
            "anim_type": "alpha",
            "duration": 0,
            "from": 1,
            "to": 0,
        }
    }
    custom_root.update(alpha_out)

    # Add the factory.

    factory = {
        "{name}_video_factory".format(name=namespace): {
            "type": "panel",
            "factory": {
                "name": "hud_actionbar_text_factory",
                "control_ids": {
                    "hud_actionbar_text": "{name}_content_panel@{name}.{name}_content_panel".format(name=namespace)
                }
            }
        },
    }

    # Merge the factory with the root.
    custom_root.update(factory)

    # Define black screen space to hide other things.
    black = {
        "black_bg": {
            "type": "image",
            "texture": "textures/ui/Black",
            "layer": -5,
            "anims": ["@{name}.black_in".format(name=namespace)],
            "alpha": 0
        }
    }

    # Merge the black bg with the root and the content panel.
    custom_root.update(black)
    content_panel["{custom_panel}_content_panel".format(
        custom_panel=namespace)]["controls"].append(black)

    # Black bg anims.
    black_in = {
        "black_in": {
            "anim_type": "alpha",
            "from": 0,
            "to": 1,
            "duration": 0,
            "next": "@{name}.black_wait".format(name=namespace)
        }
    }
    custom_root.update(black_in)

    duration = (len(images) * (1 / fps)) + 0.25
    black_wait = {
        "black_wait": {
            "anim_type": "wait",
            "duration": duration,
            "next": "@{name}.black_out".format(name=namespace)
        }
    }
    custom_root.update(black_wait)

    black_out = {
        "black_out": {
            "anim_type": "alpha",
            "from": 1,
            "to": 0,
            "duration": 0.5,
            "destroy_at_end": "hud_actionbar_text"
        }
    }
    custom_root.update(black_out)

    # Merge the image template into the root.
    custom_root.update(image_template)

    # Merge the content panel into the root.
    custom_root.update(content_panel)

    # Write the custom file.
    custom_file.write(json.dumps(custom_root))
    custom_file.close()

    # Define namespace.
    ui_defs = open("output/ui/_ui_defs.json", "w")

    # Root for UI defs.
    ui_defs_root = {"ui_defs": []}

    # Merge our namespace into the defs file.
    ui_defs_root["ui_defs"].append("ui/{name}.json".format(name=namespace))

    # Write the defs file.
    ui_defs.write(json.dumps(ui_defs_root))
    ui_defs.close()
