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
            project_template_path = Path (open_pype_server_root) / open_pype_project / 'tools' / 'pipeline' / 'playblast'
            project_template_path.mkdir(parents=True, exist_ok=True)
            return project_template_path

class VersionUtils:  
    """
    Test
    vf = VersionUtils.getVersionFolders("Y:/PROJECTS/99991_cgDev/shots/sh010/publish/render/render2d_animDeadline")
    print (vf)
    print (VersionUtils.getVersionString(vf))
    """  
    versionStr = 'v'
    versionDefault = f'{versionStr}{1:03d}'
        
    @classmethod
    def getVersionFolders(cls, rootDir, latest=True):         
        versionDirs = []   
        vDefault = f'v{1:03d}'   
        p = Path(rootDir)
        
        if not p.is_dir():
            p.mkdir(parents=True, exist_ok=True) 
            
        if p.is_dir():            
            for path in p.iterdir():
                if path.is_dir():  
                    lastDir = PurePath(path).name 
                    if lastDir.startswith(cls.versionStr):                                     
                        versionDirs.append(lastDir)  
            if len(versionDirs) > 0 :
                versionDirs.sort(reverse=True)
                return versionDirs[0]
            else:
                return None
        else:
            return None
           
    @classmethod
    def getVersionString(cls, vStr, up=True):
        if vStr!= None:
            vNumber =  vStr.lstrip('v')
            vInt = int(vNumber)
            print (vInt)
            if up:
                vInt +=1
            else:
                vInt -=1
            return f'v{vInt:03d}'
        else:
            return cls.versionDefault