from . import utils
from pathlib import Path
from .. import PLAYBLAST_PLUS_MODULE_ROOT

"""settings

Decided to opt for a getter method on this module to avoid restarting 
or reloading any host's python environment. It might be poor form to load the
config dict for each setting, but you could simply use the get_config() method 
directly to retrieve the dictionary and grab the keys you want.

# Removed - 
# CONFIG = utils.Parsing.load_json_from_file(PLAYBLAST_PLUS_MODULE_ROOT / 
#                                           'settings.json')

Returns:
    _type_: _description_
"""

def get_config() -> dict:
    return utils.Parsing.load_json_from_file(PLAYBLAST_PLUS_MODULE_ROOT / 
                                          'settings.json')
def save_config(data: dict) -> bool:
    return utils.Parsing.save_json_to_file( data , PLAYBLAST_PLUS_MODULE_ROOT / 
                                          'settings.json')

def get_ffmpeg_path() -> str :
    return (PLAYBLAST_PLUS_MODULE_ROOT / get_config()['ffmpeg']['path'] / 'ffmpeg.exe')

def get_ffprobe_path() -> str :
    return (PLAYBLAST_PLUS_MODULE_ROOT / get_config()['ffmpeg']['path'] / 'ffprobe.exe')

def get_project_template_subpath() -> str :
    return f"{get_config()['project_template_subpath']}"

def get_resources_directory() -> str :
    return (PLAYBLAST_PLUS_MODULE_ROOT / 'resources')

def get_ffmpeg_input_args() -> str :
    return f"{get_config()['ffmpeg']['input_args']}"

def get_ffmpeg_output_args() -> str :
    return f"{get_config()['ffmpeg']['output_args']}"

def open_pype_enabled() -> bool :
    return bool(get_config()['openpype'])

# if __name__ == '__main__':
#     CONFIG = refresh()
