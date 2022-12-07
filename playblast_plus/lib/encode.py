import subprocess

from lib import settings
from pathlib import Path

"""
Full credit goes to Chris Zurbrigg for this code 

Correct Argument List -
-y -framerate 24 -i [INPUTFILE]_%04d.png -c:v libx264 -pix_fmt yuv420p 
    -crf 21 -preset ultrafast [OUTPUTFILE].mp4

Ensure -pix_fmt yuv420p is present to create playable media. 
Otherwise there will be issues with black frames
"""

FFMPEG_PATH = settings.get_ffmpeg_path()
FFPROBE_PATH = settings.get_ffprobe_path()

# print ( f'ffmpeg_path {ffmpeg_path}\\ffmpeg.exe')

def extract_middle_image(source_path, output_path):

    ffprobe_cmd = f'"{FFPROBE_PATH}"'
    ffprobe_cmd += f' -v error -show_entries format=duration '
    ffprobe_cmd += f'-of default=noprint_wrappers=1:nokey=1 '
    ffprobe_cmd += source_path

    duration = float(subprocess.check_output(ffprobe_cmd))

    ffmpeg_cmd = f'"{FFMPEG_PATH}"'
    ffmpeg_cmd += ' -y -i {0} -ss {1} -frames:v 1 {2}'.format(source_path, 
                                                              duration/2.0, 
                                                              output_path)
    print(f'FFMPEG FULL COMMAND (extract_middle_image) - {ffmpeg_cmd}')
    subprocess.call(ffmpeg_cmd)

def mp4_from_image_sequence(image_seq_path, 
                            output_path, 
                            framerate=24, 
                            crf=21, 
                            preset="ultrafast", 
                            audio_path=None,
                            post_open=True
                        ):

    # ffmpeg_cmd = f'"{FFMPEG_PATH}"'
    # ffmpeg_cmd += ' -y'
    # ffmpeg_cmd += f' -framerate {framerate}'
    # ffmpeg_cmd += f' -i "{image_seq_path}"'

    # if audio_path:
    #     ffmpeg_cmd += f' -i "{audio_path}"'
    # if audio_path:
    #     ffmpeg_cmd += f' -c:a aac -filter_complex "[1:0] apad" -shortest'

    # ffmpeg_cmd += f' {settings.get_ffmpeg_input_args()}'
    # ffmpeg_cmd += f' "{output_path}"'



    ffmpeg_cmd = (
        f'{FFMPEG_PATH} -y '
        f'-framerate {framerate} '
        f'-i "{image_seq_path}" '

        f'{settings.get_ffmpeg_input_args()} '
        f'"{output_path}"'
    )

    print(f'FFMPEG FULL COMMAND (mp4_from_image_sequence) - {ffmpeg_cmd}')
    subprocess.call(ffmpeg_cmd)

    # check output fie exists
    if Path(output_path).exists() and post_open:
        # open the video file
        print(f'"{output_path}"')
        import os
        os.startfile(output_path)
        # subprocess.run(['open', f'"{output_path}"'])