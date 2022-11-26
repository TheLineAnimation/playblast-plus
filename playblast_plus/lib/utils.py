import json
from pathlib import Path

from typing import Union, str, dict, list

class ParsingUtils:
    @staticmethod
    def load_json_from_file(file: str) -> dict: 
        with open(file, 'r') as myfile:
            data=myfile.read()
        return json.loads(data)

    @staticmethod
    def get_templates(dir: str) -> list:
        _enum_items = []  
        template_dir = Path(dir)
        if template_dir.exists():
            template_files = template_dir.glob('*.json')            
            if template_files:
                _enum_items.clear()
                for t in template_files:
                    _enum_items.append((t.stem, t.stem, ""))        
        return _enum_items

class VersionUtils:  
    """
    """  
    str : versionStr = 'v'
    str : versionDefault = f'{versionStr}{1:03d}'
        
    @classmethod
    def get_version_folders(cls, rootDir: str, latest: bool = True) -> Union[str,None]:         
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
    def get_version_string(cls, vStr: str , up: bool = True) -> str:
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
