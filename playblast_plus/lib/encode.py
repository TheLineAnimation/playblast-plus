import subprocess

from lib import settings
from pathlib import Path

"""
Full credit goes to Chris Zurbrigg for this code, updated to use f-strings 
for FFMPEG process command. 

Ensure -pix_fmt yuv420p is present to create playable media. 
Otherwise there will be issues with black frames
"""

FFMPEG_PATH = settings.get_ffmpeg_path()
FFPROBE_PATH = settings.get_ffprobe_path()

def extract_middle_image(source_path: str, output_path: str):

    ffprobe_cmd = (
        f'{FFPROBE_PATH} '
        f' -v error -show_entries format=duration '
        f'-of default=noprint_wrappers=1:nokey=1 '
        f'"{source_path}"'
    )

    duration = float(subprocess.check_output(ffprobe_cmd))

    ffmpeg_cmd = (
        f'{FFMPEG_PATH} '
        f'-y ' # overwrite
        f'-i "{source_path}" '
        f'-ss "{duration/2.0}" '
        f'-frames:v 1 '
        f'"{output_path}"'
    )

    print(f'FFMPEG FULL COMMAND (extract_middle_image) - {ffmpeg_cmd}')
    subprocess.call(ffmpeg_cmd)

def mp4_from_image_sequence(image_seq_path: str, 
                            output_path: str, 
                            framerate: int = 24, 
                            audio_path: str = None,
                            post_open: bool = False
                        ):
    """_summary_

    Args:
        image_seq_path (str): _description_
        output_path (str): _description_
        framerate (int, optional): _description_. Defaults to 24.
        audio_path (_type_, optional): _description_. Defaults to None.
        post_open (bool, optional): _description_. Defaults to False.
    """

    audio_input = f' -i "{audio_path}" ' if audio_path else f''
    audio_params = (
        f' -c:a aac -filter_complex "[1:0] apad" -shortest ' 
        if audio_path else f''
    )

    ffmpeg_cmd = (
        f'{FFMPEG_PATH} '
        f'-framerate {framerate} '
        f'-y ' # overwrite
        f'-i "{image_seq_path}" '
        f'{audio_input}'
        f'{settings.get_ffmpeg_input_args()} '
        # f'-pix_fmt yuv420p '
        f'{audio_params}'
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

