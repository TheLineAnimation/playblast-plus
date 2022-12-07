import json
from pathlib import Path
from typing import Union #, dict, list
import re 



class Parsing:
    """
    Functions to process file strings for certain operations.
    """

    @staticmethod
    def load_json_from_file(file: str) -> dict:
        """Parses a JSON file from the location specified 

        Args:
            file (str): Path to the file. This should have been validated
                        before calling this function.

        Returns:
            dict: The JSON data parsed into a dictionary
        """
        with open(file, 'r') as myfile:
            data=myfile.read()
        return json.loads(data)

    @staticmethod
    def get_templates(dir: str) -> list:
        """Scans a driectory for JSON files

        Args:
            dir (str): Root folder location to search for files. Not recursive.
        Returns:
            list: A list of JSON files
        """
        _enum_items = []  
        template_dir = Path(dir)
        if template_dir.exists():
            template_files = template_dir.glob('*.json')            
            if template_files:
                _enum_items.clear()
                for t in template_files:
                    _enum_items.append((t.stem, t.stem, ""))        
        return _enum_items

    @staticmethod
    def create_ffmpeg_input(img_start: Path) -> str:
        """_summary_

        Args:
            img_start (Path): Path object to the first image sequence

        Returns:
            str: A new, formated path string containing the 
                ffmpeg padding characters.
        """
        if img_start:
            file_name = img_start.name
            # if name matches a regex pattern with a number of digits
            m = re.search(r"(?<=_|.)\d{2,}(?=\d*\.)", file_name)
            if m :
                file_sequence_padding = m.group()
                pad_length = len(file_sequence_padding)
                ffpmeg_input = file_name.replace(file_sequence_padding, 
                                f'%0{pad_length}d')
                return str(img_start.parent / ffpmeg_input)


class FolderOps:  
    """
    Static class containing useful file operations
    """  
    
    VERSION_STR :str = 'v'
    VERSION_DEFAULT:str = f'{VERSION_STR}{1:03d}'
    EXTENSION_DEFAULT:str = '.png'
        
    @classmethod
    def get_version_folders(cls, rootDir: str, latest: bool = True) -> Union[str,None]:
        """_summary_

        Args:
            rootDir (str): The roor directory as a string
            latest (bool, optional): Returns a string of the last version
                                     folder found. Defaults to True.

        Returns:
            Union[str,None]: Returns the version folder string or none if no
                             folders are found. This version string can then be 
                             used with FolderUtils.nextVersion()

        """
        versionDirs = []   
        vDefault = f'v{1:03d}'   
        p = Path(rootDir)
        if not p.is_dir():
            p.mkdir(parents=True, exist_ok=True)  
        if p.is_dir():            
            for path in p.iterdir():
                if path.is_dir():  
                    lastDir = Path(path).name 
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
    def next_version(cls, vStr: str , up: bool = True) -> str:
        """Takes a version string and returns the next version 
           as a string - e.g. 'v005' returns 'v006'.

        Args:
            vStr (str): The version number (from a folder name)
            up (bool, optional): Decides if the value returned is a version up 
            from the last folder supplied. Defaults to True.

        Returns:
            str: _description_
        """
        if vStr!= None:
            vNumber =  vStr.lstrip('v')
            vInt = int(vNumber)
            vInt +=1
            return f'v{vInt:03d}'
        else:
            return cls.VERSION_DEFAULT


    @classmethod
    def getImageSequence(cls, dir: str, ext: str) -> Path:
        """
        Looked into being able to glob multiple filetpyes, then decided after the
        code looked confusing that it really wasn't necessary. You'll always set
        the format in the Maya playblast so it's not needed. This is a simple glob
        call via Pathlib. 

        Args:
            dir (str): Root directory of the file sequence 
            ext (str, optional): the image file extension. Defaults to 'png'.

        Returns:
            Path: The first image in the found sequence
        """
        if not ext:
            ext = cls.EXTENSION_DEFAULT

        dirPath = Path(dir)
        if dirPath.exists():
            sequence = dirPath.glob(f'*{ext}')  
            return next(sequence)



# if __name__ == '__main___':
#     test_directory = r"C:\Users\pete\OneDrive\Desktop\UNIQUE ORGANISATION SYSTEM\SENDS_CLIENT_10052022\Thresh\pb"
#     img_seq_start = FolderUtils.getImageSequence(test_directory,ext=".jpg")

#     print (img_seq_start)

#     if img_seq_start:
#         ffmpeg_input_string = ParsingUtils.create_ffmpeg_input(img_seq_start)
#         print ( ffmpeg_input_string )

