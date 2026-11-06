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

# ---------------------------------------------------------------------------
# AYON style burnin
# Matches the default AYON ExtractBurnin profile for Maya reviews
# (ayon+settings://core/publish/ExtractBurnin, "focal_length_burnin"), so
# local playblasts look like published reviews. The folder (shot) name is
# only shown when AYON_FOLDER_PATH is set, so it works without AYON too:
#
#   TOP_LEFT       {yy}-{mm}-{dd}
#   TOP_CENTERED   {focalLength:.2f} mm
#   TOP_RIGHT      {anatomy[version]}   -> workfile version here
#   BOTTOM_CENTERED {folder[name]}
#   BOTTOM_RIGHT   {frame_start}-{current_frame}-{frame_end}
# ---------------------------------------------------------------------------
# Sizes are in pixels at the reference height (AYON's values at 1080p) and are
# scaled to the real frame height, so the burnin is the same proportion of the
# image at any resolution: font 30px @1080 = 2.78% of the frame height.
BURNIN_REFERENCE_HEIGHT = 1080
BURNIN_MIN_FONT_SIZE = 12

BURNIN_OPTIONS = {
    'font_size': 30,
    'font_color': ('white', 0.8),
    'bg_color': ('black', 0.5),
    'x_offset': 0,
    'y_offset': 5,
    'bg_padding': 5,
}


def get_image_size(image_seq_path: str, start_frame: int = 0):
    """Return (width, height) of the first image of a sequence, or None."""
    cmd = (
        f'"{FFPROBE_PATH}" -v error -start_number {int(start_frame)} '
        f'-i "{image_seq_path}" -select_streams v:0 '
        f'-show_entries stream=width,height -of csv=p=0'
    )
    try:
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        width, height = [int(v) for v in out.strip().split(',')[:2]]
        return width, height
    except Exception as e:
        Logger.warning(f'Could not read image size ({e}), using 1080p sizes')
        return None


def scaled_burnin_options(frame_height: int = None) -> dict:
    """BURNIN_OPTIONS scaled from the reference height to frame_height."""
    opts = dict(BURNIN_OPTIONS)
    if not frame_height:
        return opts
    scale = frame_height / float(BURNIN_REFERENCE_HEIGHT)
    opts['font_size'] = max(BURNIN_MIN_FONT_SIZE,
                            int(round(opts['font_size'] * scale)))
    for key in ('x_offset', 'y_offset', 'bg_padding'):
        opts[key] = int(round(opts[key] * scale))
    return opts

BURNIN_FONT = (Path(__file__).parent.parent / 'resources' / 'fonts' /
               'LiberationSans-Regular.ttf')


def _escape_drawtext(text: str) -> str:
    """Escape a literal string for use inside drawtext text='...'."""
    return (str(text)
            .replace('\\', '\\\\')
            .replace("'", '')
            .replace(':', '\\:')
            .replace(',', '\\,')
            .replace('%', '\\%'))


def _escape_path(path) -> str:
    return Path(path).as_posix().replace(':', '\\:')


def build_ayon_burnin_filter(framerate, start_frame, frame_count,
                             burnin_data: dict, temp_files: list,
                             frame_height: int = None):
    """Write an ffmpeg filter script that draws the AYON style burnin.

    Args:
        burnin_data (dict): date, version, folder (str) and
            focal_lengths (list of float, one per frame).
        temp_files (list): created files are appended so they can be removed.
        frame_height (int): image height, used to scale the burnin.

    Returns:
        str|None: path to the filter script.
    """
    import tempfile
    opts = scaled_burnin_options(frame_height)
    Logger.info(f"Burnin font size {opts['font_size']}px "
                f"(frame height {frame_height})")

    font = BURNIN_FONT
    if not font.is_file():
        font = Path('C:/Windows/Fonts/arial.ttf')

    end_frame = int(start_frame) + int(frame_count) - 1
    pad = len(str(end_frame))
    frame_text = (f'{int(start_frame)}-'
                  f'%{{eif\\:n+{int(start_frame)}\\:d\\:{pad}}}-{end_frame}')

    focal_lengths = burnin_data.get('focal_lengths') or []
    focal_text = f'{focal_lengths[0]:.2f} mm' if focal_lengths else ''
    focal_animated = len(set(round(f, 2) for f in focal_lengths)) > 1

    y_top = f"{opts['y_offset']}"
    y_bottom = f"h-text_h-{opts['y_offset']}"
    x_left = f"{opts['x_offset']}"
    x_center = "w/2-tw/2"
    x_right = f"w-tw-{opts['x_offset']}"

    slots = [
        # (label, text, x, y, already_escaped)
        ('tl', _escape_drawtext(burnin_data.get('date', '')), x_left, y_top),
        ('tc', _escape_drawtext(focal_text), x_center, y_top),
        ('tr', _escape_drawtext(burnin_data.get('version', '')), x_right, y_top),
        ('bc', _escape_drawtext(burnin_data.get('folder', '')), x_center, y_bottom),
        ('br', frame_text, x_right, y_bottom),
    ]

    font_color, font_alpha = opts['font_color']
    bg_color, bg_alpha = opts['bg_color']

    filters = []

    # animated focal length: update the top centre text on each frame
    if focal_animated:
        lines = []
        for i, focal in enumerate(focal_lengths):
            seconds = i / float(framerate)
            lines.append(f"{seconds:.6f} drawtext@tc reinit "
                         f"text='{_escape_drawtext(f'{focal:.2f} mm')}';")
        with tempfile.NamedTemporaryFile('w', suffix='.cmd', delete=False,
                                         encoding='utf-8') as f:
            f.write('\n'.join(lines))
        temp_files.append(f.name)
        filters.append(f"sendcmd=f='{_escape_path(f.name)}'")

    for label, text, x, y in slots:
        if not text:
            continue
        filters.append(
            f"drawtext@{label}=fontfile='{_escape_path(font)}'"
            f":text='{text}'"
            f":x={x}:y={y}"
            f":fontcolor={font_color}@{font_alpha}"
            f":fontsize={opts['font_size']}"
            f":box=1:boxcolor={bg_color}@{bg_alpha}"
            f":boxborderw={opts['bg_padding']}"
        )

    if not filters:
        return None

    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False,
                                     encoding='utf-8') as f:
        f.write(',\n'.join(filters))
    temp_files.append(f.name)
    return f.name


def mp4_from_image_sequence(image_seq_path: str,
                            output_path: str, 
                            framerate: int = 24,
                            start_frame: int = 0, 
                            end_frame: int = 0,
                            audio_path: str = None,
                            audio_offset: float = 0.0,
                            post_open: bool = False,
                            viewer_arg='start',
                            add_burnin: bool = False,
                            burnin_data: dict = None,
                            fast: bool = False,
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
        post_open (bool): whether to open the video after creation.
        viewer_arg (str): the viewer argument to pass to ffmpeg.

    Full credit goes to Chris Zurbrigg for this code, updated to use f-strings 
    for FFMPEG process command, and some additional arguments. 

    Enabled log level quiet as a default now it seems to be working nicely, but 
    perhaps this could be exposed as a local setting. 
    """

    # NOTE: end_frame is the number of frames to encode, not a frame number.
    frame_count = int(end_frame)

    temp_files = []
    burnin = ''
    if add_burnin:
        image_size = get_image_size(image_seq_path, start_frame)
        filter_script = build_ayon_burnin_filter(
            framerate=framerate,
            start_frame=start_frame,
            frame_count=frame_count,
            burnin_data=burnin_data or {},
            temp_files=temp_files,
            frame_height=image_size[1] if image_size else None,
        )
        if filter_script:
            burnin = f'-filter_script:v "{filter_script}" '

    # --- audio -------------------------------------------------------------
    # audio_offset = seconds into the audio file that line up with the first
    # video frame. Positive: skip the start of the audio. Negative: the sound
    # starts later, so pad silence in front of it.
    audio_input = ''
    audio_params = ''
    if audio_path and Path(audio_path).is_file():
        audio_filters = []
        if audio_offset > 0:
            audio_input = f'-ss {audio_offset:.4f} -i "{audio_path}" '
        else:
            audio_input = f'-i "{audio_path}" '
            if audio_offset < 0:
                delay_ms = int(round(-audio_offset * 1000))
                audio_filters.append(f'adelay={delay_ms}:all=1')
        # pad with silence so the audio is never shorter than the video
        audio_filters.append('apad')
        audio_params = (
            f'-map 1:a:0 -c:a aac -b:a 192k '
            f'-af "{",".join(audio_filters)}" '
        )
    elif audio_path:
        Logger.warning(f'Audio file not found, skipping audio : {audio_path}')

    duration = frame_count / float(framerate) if framerate else 0

    # fast mode: lighter, quicker encode (speed over quality)
    video_args = (settings.get_ffmpeg_fast_input_args() if fast
                  else settings.get_ffmpeg_input_args())

    # FFmpeg option order matters: input options, then all inputs,
    # then output options, then the output file.
    ffmpeg_cmd = (
        f'"{FFMPEG_PATH}" '
        f'-y '  # overwrite
        f'-loglevel error '
        f'-framerate {framerate} '
        f'-start_number {start_frame} '
        f'-i "{image_seq_path}" '
        f'{audio_input}'
        f'-map 0:v:0 '
        f'{burnin}'
        f'{video_args} '
        f'{audio_params}'
        f'-frames:v {frame_count} '
        + (f'-t {duration:.4f} ' if audio_params and duration else '')
        + f'"{output_path}"'
    )

    Logger.info(f'FFMPEG COMMAND (mp4_from_image_sequence) : {ffmpeg_cmd}')
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        Logger.error(f'FFMPEG failed ({result.returncode}) : {result.stderr}')

    for temp_file in temp_files:
        try:
            Path(temp_file).unlink()
        except OSError:
            pass

    # check output fie exists
    if Path(output_path).exists() and post_open:
        # open the video file
        Logger.info(f'OUTPUT PATH ENCODE  (mp4_from_image_sequence) : {output_path}')
        open_media_file(output_path, viewer_arg)
        
