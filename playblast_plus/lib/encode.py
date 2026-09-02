"""
Full credit goes to Chris Zurbrigg for this code, updated to use f-strings 
for FFMPEG process command. 

Ensure -pix_fmt yuv420p is present to create playable media. 
Otherwise there will be issues with black frames
"""

import subprocess

from . import settings
from pathlib import Path

from .logger import Logger



FFMPEG_PATH = settings.get_ffmpeg_path()
FFPROBE_PATH = settings.get_ffprobe_path()

def open_media_file(filepath:str, viewer:str='start'):
    """Opens the supplied mp4 or image file in the OS preferred viewer, 
    or a supplied custom viewer.

    Args:
        filepath (str): Path to the media that needs to be viewed
        viewer (str, optional): A path to a viewer executable. Can be specified 
        per user in the local settings.json _. Defaults to 'start'.
    """

    # open the file (video or jpg)
    # this should open the OS defined executable for the file type

    check_viewer = Path(viewer)

    if viewer != 'start':
        Logger.info(f'Checking custom viewer path : "{viewer}"')

    if check_viewer.is_file():
        Logger.info(f'Launching : {check_viewer.stem} : "{filepath}"')
        subprocess.Popen([viewer,filepath],shell=False)
        return
    else:
        Logger.info(f'Launching default viewer : "{filepath}"')
        import os
        os.startfile(f'"{filepath}"')
        # subprocess.Popen(['start', filepath ],shell=True)

def extract_middle_image(source_path: str, output_path: str):
    """
    Takes a sequence and locates the middle image. This is useful for preview
    thumbnails when the start image might not indicate the contents. 

    Args:
        source_path (str): The path to the sequence
        output_path (str): The output image

    Full credit goes to Chris Zurbrigg for this code, updated to use f-strings 
    for FFMPEG process command. 
    """

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

    Logger.info(f'FFMPEG COMMAND (extract_middle_image) : {ffmpeg_cmd}')
    subprocess.call(ffmpeg_cmd)

def get_audio_sync_args(start_frame: int, audio_offset_frame: float, 
                        framerate: int) -> tuple:
    """
    Works out how FFMPEG should sync an audio track to a given start frame, 
    based on the frame the audio was offset to start playing from in the 
    host's timeline.

    If the video starts after the audio (audio_offset_frame is before 
    start_frame), the audio is trimmed with -ss so it lines up with the 
    first rendered frame. If the video starts before the audio 
    (audio_offset_frame is after start_frame), an "adelay" audio filter is 
    used to insert real silence ahead of the audio until it should start 
    playing.

    Note: -itsoffset is deliberately avoided for the delay case. It only 
    shifts container timestamps, which is unreliable when muxed against an 
    image sequence input (the silence is often dropped entirely instead of 
    being inserted) - "adelay" writes actual silent samples so playback is 
    genuinely in sync, and is compatible with the "apad" filter already used 
    to pad the end of a shorter audio track.

    Args:
        start_frame (int): the first frame included in the video.
        audio_offset_frame (float): the frame the audio starts playing from.
        framerate (int): the framerate of the scene/output video.

    Returns:
        tuple: (seek_args (str), filter_args (str))
            seek_args is an FFMPEG input option to place before the audio 
            "-i", used for the trim case.
            filter_args is an audio filter chain fragment to prepend inside 
            the audio "-filter_complex", used for the delay case.
    """

    seconds_offset = (start_frame - audio_offset_frame) / float(framerate)

    if seconds_offset >= 0:
        return (f'-ss {seconds_offset} ', '')
    else:
        delay_ms = round(abs(seconds_offset) * 1000)
        return ('', f'adelay={delay_ms}:all=1,')

def mp4_from_image_sequence(image_seq_path: str, 
                            output_path: str, 
                            framerate: int = 24,
                            start_frame: int = 0, 
                            end_frame: int = 0,
                            audio_path: str = None,
                            audio_offset_frame: float = 0,
                            post_open: bool = False,
                            viewer_arg='start',
                            add_burnin: bool = False,
                            burnin_text: str = "",
                            burnin_font_size: int = 24
                            ):
    
    """
    Create a video from a sequence of images.  

    Args:
        image_seq_path (str): the path to the image sequence folders.
        output_path (str): the path to the output video.
        framerate (int): the framerate of the output video.
        start_frame (int): the first frame to include in the video.
        end_frame (int): the last frame to include in the video.
        audio_path (str): the path to the audio file to include in the video.
        audio_offset_frame (float): the frame the audio starts playing from
            in the host's timeline. Used to keep the audio in sync with the
            rendered frame range.
        post_open (bool): whether to open the video after creation.
        viewer_arg (str): the viewer argument to pass to ffmpeg.

    Full credit goes to Chris Zurbrigg for this code, updated to use f-strings 
    for FFMPEG process command, and some additional arguments. 

    Enabled log level quiet as a default now it seems to be working nicely, but 
    perhaps this could be exposed as a local setting. 
    """

    if add_burnin:
        burnin = (
            f'-vf "drawtext=font=Consolas: fontsize={burnin_font_size}: '
            f'fontcolor=white@0.5: text=\'{burnin_text} | %{{eif\:n\:d\:4}}\': '
            f'start_number={start_frame}: r=24: x=(w-tw-20): y=h-lh-20: '
            f'box=1: boxcolor=black@0.5: boxborderw=2"'
        )
    else:
        burnin = ''        

    audio_delay_filter = ''

    if audio_path:
        audio_seek, audio_delay_filter = get_audio_sync_args(
            start_frame, audio_offset_frame, framerate)
        audio_input = f' {audio_seek}-i "{audio_path}" '
    else:
        audio_input = f''

    audio_params = (
        f' -c:a aac -filter_complex "[1:0] {audio_delay_filter}apad" -shortest ' 
        if audio_path else f''
    )

    ffmpeg_cmd = (
        f'"{FFMPEG_PATH}" '
        f'-framerate {framerate} '
        f'-y ' # overwrite
        f'-start_number {start_frame} '
        f'-loglevel quiet ' 
        f'-i "{image_seq_path}" '
        f'{burnin} '
        f'{audio_input}'
        f'{settings.get_ffmpeg_input_args()} '
        f'{audio_params}'
        f'-frames:v {end_frame} '
        f'"{output_path}"'
    )

    Logger.info(f'FFMPEG COMMAND (mp4_from_image_sequence) : {ffmpeg_cmd}')
    subprocess.call(ffmpeg_cmd)

    # check output fie exists
    if Path(output_path).exists() and post_open:
        # open the video file
        Logger.info(f'OUTPUT PATH ENCODE  (mp4_from_image_sequence) : {output_path}')
        open_media_file(output_path, viewer_arg)
        
