
from .lib.host import Host as host
from . import version


def run():
    HOST = host.get_name()

    if HOST == 'maya':
        from .hosts.maya import ui
        ui.run(version)

    elif HOST == '3dsmax':
        from .hosts.max import max_scene
        print (f'Current Maxfile : {max_scene.Max_Scene.get_name()}')
        from .hosts.max import ui
        ui.run(version)

        