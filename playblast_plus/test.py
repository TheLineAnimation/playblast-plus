

from pathlib import Path
import lib.settings as settings
import lib.utils as utils
import lib.preset as preset
# import lib.encode as encode
# import hosts.maya as maya

"""
Load the global settings from the JSON file
"""
settings_dict = utils.Parsing.load_json_from_file('.\settings.json')
settings_dict['openpype']
print (settings.open_pype_enabled())
print ( f'settings {settings_dict}')

ffmpeg_path = Path(settings_dict['ffmpeg']['path']).resolve()
print ( f'ffmpeg_path {ffmpeg_path}\\ffmpeg.exe')

"""
Get the locations of the templates and load them 
"""
st = (settings_dict['studio_templates'])
paths = preset.get_project_locations (st)
templates = preset.load_templates ( paths )
print ( f'templates {templates}')

"""
Test encoding 
"""
#test_directory = r"C:\Users\pete\OneDrive\Desktop\UNIQUE ORGANISATION SYSTEM\SENDS_CLIENT_10052022\Thresh\pb"

#test_directory = r"C:\Users\pete\OneDrive\Desktop\pb\pb"

#img_seq_start = utils.FolderOps.getImageSequence(test_directory,ext=".jpg")

# print (img_seq_start)

#if img_seq_start:
    #ffmpeg_input_string = utils.Parsing.create_ffmpeg_input(img_seq_start)
    # print ( ffmpeg_input_string )

    #output_path = test_directory + '\local_playblast.mp4'

    # encode.mp4_from_image_sequence(ffmpeg_input_string,
    #                         output_path, 
    #                         framerate=24, 
    #                         # audio_path=r"C:\Users\pete\OneDrive\Documents\Files\Rigs\Frameworks\AdvancedSkeleton5\Install\AdvancedSkeleton5Files\div\sound\exampleVoice.wav"
    #                         post_open=False
    #                     )

    #thumbnail = utils.Parsing.create_ffmpeg_still_frame_output(output_path, "middle_frame_test")
    #print (thumbnail)

    #encode.extract_middle_image(output_path, thumbnail)

# import re
# img = "C:\Users\pete\OneDrive\Documents\maya\projects\default\playblasts\playblast_side_pete_TEST.####.png"
# m = re.search(r"/(\#{3,})", img)
# if m :
#     file_sequence_padding = m.group()
#     pad_length = len(file_sequence_padding)
#     ffpmeg_input = img.replace(file_sequence_padding, 
#                     f'%0{pad_length}d')
#     print (ffpmeg_input)