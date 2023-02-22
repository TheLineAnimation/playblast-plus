import playblast_plus

from pathlib import Path

from ...lib import utils as utils
from ...lib import settings as settings
from ...lib import preset as preset
from ...lib import encode as encode

from ...hosts.maya import capture as capture
from ...hosts.maya import tokens as tokens
from ...hosts.maya import maya_scene as maya_scene

# WEDS - SETUP TOKENS!!!

# import maya.cmds as cmds 

print (settings.CONFIG )

from playblast_plus import PLAYBLAST_PLUS_MODULE_ROOT as module_root

paths = preset.get_project_locations (str(playblast_plus.PLAYBLAST_PLUS_MODULE_ROOT / settings.CONFIG['studio_templates'] ))
templates = preset.load_templates ( paths )

playblast_dir = maya_scene.get_playblast_dir()
output_name = (tokens.format_tokens('<scene>_<camera>_<user>_what',None))

default_template = templates[0]['default']
default_template["filename"] = f'{playblast_dir}\{output_name}'
# default_template["compression"] = "png"
# default_template["format"] = "image"
camera = cmds.ls(selection=True, dag=True, leaf=True, type="camera")
default_template["camera"] = camera[0]
# default_template["show_ornaments"] = False
# default_template["viewer"] = False
# default_template["frame_padding"] = 4

# import pprint
# pprint.pprint(default_template)

if default_template["frame_padding"] > 4:
    # convert to logger in actual UI code
    print ("Playblast padding should be set to 4 to allow output transcode compatibility - This value will be set automatically.")


filename = capture.capture(**default_template)
print (filename)

ffmpeg_input_string = utils.Parsing.playblast_output_to_ffmpeg_input(filename)

output_path = f'{playblast_dir}\{output_name}.mp4'

encode.mp4_from_image_sequence(ffmpeg_input_string,
                        output_path, 
                        framerate=24, 
                        post_open=True
                    )



snap_image_filename = (tokens.format_tokens('<playblast_dir>\captures\<scene>_<camera>_<user>_CAPTURE',None))

default_template["filename"] = snap_image_filename

# snap_image = capture.snap(width=4000, height=4000, maintain_aspect_ratio=False, **default_template)
# print (snap_image)

# snap_clip_image = capture.snap(clipboard=True,**default_template)
# print (snap_clip_image)


# capture.capture('persp1', 800, 600,
#         viewport_options={
#             "displayAppearance": "wireframe",
#             "grid": False,
#             "polymeshes": True,
#         },
#         camera_options={
#             "displayResolution": True
#         }
# )