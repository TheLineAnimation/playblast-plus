import os
from pathlib import Path, PurePath

"""
MAYA_APP_DIR
"""

OPEN_PYPE_PROJECT_ROOT = None

def open_pype_enabled() -> bool:
    """
    Check if there is a project pipeline. AVALON_PROJECT env won't be set 
    without it, so there's not much else we need
    """
    return os.getenv("AVALON_PROJECT")

def get_open_pype_template_location() -> str:

    if open_pype_enabled():
        open_pype_server_root = os.getenv("OPENPYPE_PROJECT_ROOT_WORK") 
        open_pype_project = os.getenv("AVALON_PROJECT")

        if open_pype_server_root and open_pype_project:
            project_template_path = ( Path (open_pype_server_root) / 
                                        open_pype_project / 
                                        'tools' / 
                                        'pipeline' / 
                                        'playblast'
                                    )
            project_template_path.mkdir(parents=True, exist_ok=True)
            return project_template_path

