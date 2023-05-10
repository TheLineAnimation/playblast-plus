from .lib.dcc import Host
from .lib import settings
from pathlib import Path

def download_window(url, locations, main_window):
    from .lib import widgets
    downloader = widgets.DownloadWindow(url, locations, main_window)
    downloader.show()

def run():
    """
    settings.get_ffmpeg_path() checks the list of executables in the config.json
    """
    ffmpeg_path = settings.get_ffmpeg_path()
    if ffmpeg_path and Path(ffmpeg_path).exists():
        from . import ui, version
        ui.run(version=version)
    else:
        url = settings.get_ffmpeg_download_url()
        locations =settings.resolve_ffmpeg_paths()
        download_window(url,locations, Host().main_window)



        