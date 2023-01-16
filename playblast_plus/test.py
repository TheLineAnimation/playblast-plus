import lib.preset as preset

import lib.settings as settings

import lib.utils as utils
import lib.encode as encode


# from pathlib import Path
# settings = preset.load_json('.\settings.json')


# settings['openpype']
# st = (settings['studio_templates'])
# paths = preset.get_project_locations (st)
# templates = preset.load_templates ( paths )

# print ( f'settings {settings}')
# print ( f'templates {templates}')

print (settings.CONFIG)
print (settings.open_pype_enabled())

# ffmpeg_path = Path(settings['ffmpeg']['path']).resolve()
# print ( f'ffmpeg_path {ffmpeg_path}\\ffmpeg.exe')


test_directory = r"C:\Users\pete\OneDrive\Desktop\UNIQUE ORGANISATION SYSTEM\SENDS_CLIENT_10052022\Thresh\pb"

test_directory = r"C:\Users\pete\OneDrive\Desktop\pb\pb"

img_seq_start = utils.FolderOps.getImageSequence(test_directory,ext=".jpg")

# print (img_seq_start)

if img_seq_start:
    ffmpeg_input_string = utils.Parsing.create_ffmpeg_input(img_seq_start)
    # print ( ffmpeg_input_string )

    output_path = test_directory + '\local_playblast.mp4'

    # encode.mp4_from_image_sequence(ffmpeg_input_string,
    #                         output_path, 
    #                         framerate=24, 
    #                         # audio_path=r"C:\Users\pete\OneDrive\Documents\Files\Rigs\Frameworks\AdvancedSkeleton5\Install\AdvancedSkeleton5Files\div\sound\exampleVoice.wav"
    #                         post_open=False
    #                     )

    thumbnail = utils.Parsing.create_ffmpeg_still_frame_output(output_path, "middle_frame_test")
    print (thumbnail)

    encode.extract_middle_image(output_path, thumbnail)