import lib.preset as preset

CONFIG = preset.load_json('.\settings.json')

@staticmethod
def get_ffmpeg_path() -> str :
    return f"{CONFIG['ffmpeg']['path']}/ffmpeg.exe"

@staticmethod
def get_ffmpeg_input_args() -> str :
    return f"{CONFIG['ffmpeg']['input_args']}"

@staticmethod
def get_ffmpeg_output_args() -> str :
    return f"{CONFIG['ffmpeg']['output_args']}"

@staticmethod
def get_ffprobe_path() -> str :
    return f"{CONFIG['ffmpeg']['path']}/ffprobe.exe"

@staticmethod
def get_ffprobe_path() -> str :
    return f"{CONFIG['ffmpeg']['path']}/ffprobe.exe"

@staticmethod
def open_pype_enabled() -> bool :
    return bool(CONFIG['openpype'])
