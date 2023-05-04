"""
lib.settings

Decided to opt for a getter method on this module to avoid restarting 
or reloading any host's python environment. It might be poor form to load the
config dict for each setting, but you could simply use the get_config() method 
directly to retrieve the dictionary and grab the keys you want.

# Removed - 
# CONFIG = utils.Parsing.load_json_from_file(PLAYBLAST_PLUS_MODULE_ROOT / 
#                                           'settings.json')

"""

from . import utils
from pathlib import Path
from .. import PLAYBLAST_PLUS_MODULE_ROOT

def create_host_settings(path:Path):
    """
        Create the host settings dictionary. 
        This dictionary will contain the host settings for each camera.

    Args:
        path (Path): The pathlib Path to the host settings file. 
        Can be added globally now as I've regressed the notion of project templates

    Returns:
        Dict: The host settings dictionary.
    
    """
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
        "last_template": "",
        "last_playblast": "",
        "custom_viewer": ""
    }
    # host_config = Path ( path , 'pbp_settings.json')
    utils.Parsing.save_json_to_file( data , path)

def get_host_settings(path:str) -> dict:
    """
        Gives a path to a file, return the host settings dictionary.

    Args:
        path (str): The path to the file containing the host settings dictionary.
        Can be added globally now as I've regressed the notion of project templates

    Returns:
        Dict: the host settings dictionary.
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
    """Save the host settings to a file.

    Args:
        path (str): the path to the file we are saving to.
        data (dict): the data we are saving.

    Returns:
        bool: True if the save was successful, False otherwise.
    """
    user_folder = Path(path)
    if user_folder.exists and user_folder.is_dir():
        host_config = user_folder / 'pbp_settings.json'

        if host_config.is_file():
            return utils.Parsing.save_json_to_file( data , str(host_config))
    else:
        return False

def get_config() -> dict:
    """Read the config file and return a dictionary of the values.

    Returns:
        dict: The config dictionary.
    """

    return utils.Parsing.load_json_from_file(PLAYBLAST_PLUS_MODULE_ROOT / 
                                          'config.json')
def save_config(data: dict) -> bool:
    """
    Save the configuration dictionary to a file.

    Args:
        data (dict): the configuration dictionary

    Returns:
        bool: True if the file was saved successfully, False otherwise.
    """
    return utils.Parsing.save_json_to_file( data , PLAYBLAST_PLUS_MODULE_ROOT / 
                                          'config.json')
def filepath() -> str :
    """
    Return the filepath for the config dictionary.
    Returns: 
        str: The dictionary path.
    """
    return (PLAYBLAST_PLUS_MODULE_ROOT / 'config.json')

def is_FFMpeg_installed(exe:str= 'ffmpeg'):
    """
    Check if the FFMPEG is installed on the system.

    Args:
        exe (str) - the name of the executable file.
    Returns:
        bool: True if the executable is found, False otherwise.
    """
      
    config = get_config()
    if config['ffmpeg']:    
        index = 0
        exists = False
        fpaths = config['ffmpeg']['executable_paths']
        while index < len(fpaths) and not exists:
            ffmpeg_path = Path(fpaths[index]).absolute()
            # print (f'FFMPEG PATHS : {ffmpeg_path} {ffmpeg_path.exists()}') 
            exe_path = (ffmpeg_path / f'{exe}.exe')
            if exe_path.exists():
                exists = exe_path
            index += 1
        return exists
    return

def get_ffmpeg_path() -> str :
    """
    Get the path to the ffmpeg executable. This is used to convert the video files to images.
    
    Returns: 
        str: the path to the ffmpeg executable
    """
    return is_FFMpeg_installed()

def resolve_ffmpeg_paths() -> list :    
    """
    Resolve the paths to the ffmpeg executables. This is necessary because the paths are stored as relative paths.
    Returns:
        list: the list of paths to the ffmpeg executables
    """
    config = get_config()['ffmpeg']['executable_paths']
    return [Path(path).absolute() for path in config]

def get_ffprobe_path() -> str :
    """
    Get the path to the ffprobe executable. This is used to get the duration of each video.
    Returns: 
        str: the path to the ffprobe executable
    """
    return is_FFMpeg_installed('ffprobe')

def get_project_template_subpath() -> str :
    """
    Get the project template subpath. This is the subpath of the project template directory.
    Returns
        str: The subpath of the project template directory.
    """
    return f"{get_config()['project_template_subpath']}"

def get_resources_directory() -> str :
    """
    Get the resources directory for the project. This is used to find the data files.
    
    Returns: 
        str: The resources directory
    """
    return (PLAYBLAST_PLUS_MODULE_ROOT / 'resources')

def get_ffmpeg_input_args() -> str :
    """
    Get the input arguments for ffmpeg. This is used to get the input arguments for the video.
    
    Returns:
        str: The input arguments for ffmpeg.
    """
    return f"{get_config()['ffmpeg']['input_args']}"

def get_ffmpeg_output_args() -> str :
    """
    Get the ffmpeg output arguments for the video writer.
    
    Returns: 
        str: The ffmpeg output arguments for the video writer.
    """
    return f"{get_config()['ffmpeg']['output_args']}"

def get_ffmpeg_burnin_text() -> str :
    """
    Retrieve the text preset to be added into the video.
    
    Returns: 
        str: the text for the video burnin.
    """
    return f"{get_config()['ffmpeg']['burnin']['text']}"

def get_ffmpeg_download_url() -> str :
    """
    Get the ffmpeg download location for the fro FFMpeg.
    Returns: 
        str: the url string.
    """
    return f"{get_config()['ffmpeg']['download_url']}"

def get_doclink() -> str :
    """
    Get the github documentation url.
    Returns: 
        str: the url string.
    """
    return get_config()['documentation_url']


