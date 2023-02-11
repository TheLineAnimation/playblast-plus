import os
from pathlib import Path, PurePath

from . import settings

"""
MAYA_APP_DIR
"""

OPEN_PYPE_PROJECT_ROOT = None
PROJECT_TEMPLATE_SUBFOLDER = settings.get_project_template_subpath()

def open_pype_enabled() -> bool:
    """
    Check if there is a project pipeline. AVALON_PROJECT env won't be set 
    without it, so there's not much else we need

    As this is useful to enable UI states, we need to explicity return the 
    boolean value, as the env string won't be infere by PySide/QT as a 
    true/false argument. 

    """
    if os.getenv("AVALON_PROJECT"):
        return True
    else:
        return False

def get_open_pype_template_location() -> str:

    if open_pype_enabled():
        open_pype_server_root = os.getenv("OPENPYPE_PROJECT_ROOT_WORK") 
        open_pype_project = os.getenv("AVALON_PROJECT")

        if open_pype_server_root and open_pype_project:
            project_template_path = ( Path (open_pype_server_root) / 
                                        open_pype_project / 
                                        PROJECT_TEMPLATE_SUBFOLDER
                                    )
            project_template_path.mkdir(parents=True, exist_ok=True)
            return project_template_path

