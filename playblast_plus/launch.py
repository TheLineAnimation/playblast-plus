
from .lib.host import Host as host
from .lib import settings
from . import version

from pathlib import Path

def run():
    """
    settings.get_ffmpeg_path checks the list of executables in the config.json
     
    """
    HOST = host.get_name()

    ffmpeg_path = settings.get_ffmpeg_path()
    if ffmpeg_path and Path(ffmpeg_path).exists():
        if HOST == 'maya':
            from .hosts.maya import ui
            ui.run(version)
        elif HOST == '3dsmax':
            from .hosts.max import ui
            ui.run(version)
    else:
        from .lib import widgets
        if HOST == 'maya':
            from .hosts.maya.maya_scene import Maya_Scene
            main_window = Maya_Scene.main_window()
        elif HOST == '3dsmax':
            from .hosts.max.max_scene import Max_Scene
            main_window = Max_Scene.main_window()

        url = settings.get_ffmpeg_download_url()
        locations =settings.resolve_ffmpeg_paths()
        downloader = widgets.DownloadWindow(url, locations, main_window)
        downloader.show()


        