
from .lib.host import Host as host
from .lib import settings
from . import version

from pathlib import Path

def run():
    """
    settings.get_ffmpeg_path checks the list of executables in the config.json
     
    """

    ffmpeg_path = settings.get_ffmpeg_path()
    if Path(ffmpeg_path).exists():
        HOST = host.get_name()

        if HOST == 'maya':
            from .hosts.maya import ui
            ui.run(version)
        elif HOST == '3dsmax':
            from .hosts.max import ui
            ui.run(version)
    else:
        pass


        