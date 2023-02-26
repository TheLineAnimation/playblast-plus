from . import utils
from pathlib import Path
from .. import PLAYBLAST_PLUS_MODULE_ROOT

"""
settings

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

def create_host_settings(path:Path):
    data = {
        "toggle_overrides": False,
        "toggle_copy": False,
        "toggle_keep": False,
        "set_imageplane": False,
        "set_wire": False,
        "set_half": False,
        "isolate":False,
        "use_workspace": False,
        "add_burnin": False,
        "output_token": "",
        "last_camera": "",
        "last_playblast": "",
        "custom_viewer": ""
    }
    # host_config = Path ( path , 'pbp_settings.json')
    utils.Parsing.save_json_to_file( data , path)

def get_host_settings(path:str) -> dict:
    """_summary_

    Args:
        path (str): _description_

    Returns:
        dict: _description_
    """

    user_folder = Path(path)
    if not user_folder.is_dir():
        user_folder.mkdir(parents=True, exist_ok=True)

    host_config = user_folder / 'pbp_settings.json'

    if not host_config.is_file():
        create_host_settings(host_config)

    if host_config.exists:
        return utils.Parsing.load_json_from_file(str(host_config))

def save_host_settings(path:str, data: dict) -> bool:
    """_summary_

    Args:
        path (str): _description_
        data (dict): _description_

    Returns:
        bool: _description_
    """
    user_folder = Path(path)
    if user_folder.exists and user_folder.is_dir():
        host_config = user_folder / 'pbp_settings.json'

        if host_config.is_file():
            return utils.Parsing.save_json_to_file( data , str(host_config))
    else:
        return False

def get_config() -> dict:
    return utils.Parsing.load_json_from_file(PLAYBLAST_PLUS_MODULE_ROOT / 
                                          'config.json')
def save_config(data: dict) -> bool:
    return utils.Parsing.save_json_to_file( data , PLAYBLAST_PLUS_MODULE_ROOT / 
                                          'config.json')
def filepath() -> str :
    return (PLAYBLAST_PLUS_MODULE_ROOT / 'config.json')

def filepath() -> str :
    return (PLAYBLAST_PLUS_MODULE_ROOT / 'config.json')

def is_FFMpeg_installed(exe:str= 'ffmpeg'):
    config = get_config()
    if config['ffmpeg']:
        for path in config['ffmpeg']['executable_paths']:
            ffmpeg_path = Path(path)
            print (f'FFMPEG PATHS : {ffmpeg_path} {ffmpeg_path.exists()}') 
            exe_path = (ffmpeg_path / f'{exe}.exe')
            if exe_path.exists():
                return exe_path
    else:
        return False

def get_ffmpeg_path() -> str :
    return is_FFMpeg_installed()

def get_ffprobe_path() -> str :
    return is_FFMpeg_installed('ffprobe')

def get_project_template_subpath() -> str :
    return f"{get_config()['project_template_subpath']}"

def get_resources_directory() -> str :
    return (PLAYBLAST_PLUS_MODULE_ROOT / 'resources')

def get_ffmpeg_input_args() -> str :
    return f"{get_config()['ffmpeg']['input_args']}"

def get_ffmpeg_output_args() -> str :
    return f"{get_config()['ffmpeg']['output_args']}"

def get_ffmpeg_burnin_text() -> str :
    return f"{get_config()['ffmpeg']['burnin']['text']}"

def get_ffmpeg_download_url() -> str :
    return f"{get_config()['ffmpeg']['download_url']}"

