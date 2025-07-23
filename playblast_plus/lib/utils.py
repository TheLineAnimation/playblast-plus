import json
from pathlib import Path
from typing import Union #, dict, list
import re 
import subprocess

# this is an example function which retrieves the name of the current user

def get_user_name():
    """
    It returns the user's name.
    """
    import getpass
    return getpass.getuser()

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

        with open(str(file), 'r') as f:
            data=f.read()
        return json.loads(data)
    
    @staticmethod
    def save_json_to_file( data: dict, file: str):
        """Saves a JSON file to the location specified 

        Args:
            data (dict): _description_
            file (str): location of the file. 
        """       
        with open(file, 'w',encoding='utf-8') as f:
            json.dump( data , f, ensure_ascii=False, indent=4)
        # print (f'creating settings file {file}')  

    @staticmethod
    def get_templates(dir: str) -> list:
        """Scans a directory for JSON files

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
                for t in template_files:
                    _enum_items.append((t.stem, t))        
        return _enum_items

    @staticmethod
    def create_ffmpeg_input(img_start: str) -> str:
        """
            Takes an image input path, and calculates the padding via regex. 
            Then replaces this file numbering with an ffmpeg compliant string

            e.g. - preview_0001.png will become preview_%4d.png

        Args:
            img_start (Path): Path object to the first image sequence
            (this is for a non-Maya sequence where you give it the first frame 
            of a sequence)

        Returns:
            str: A new, formatted path string containing the 
                ffmpeg padding characters.
        """
        if img_start:
            img_start = Path(img_start)
            file_name = img_start.name
            # if name matches a regex pattern with a number of digits
            m = re.search(r"(?<=_|.)\d{2,}(?=\d*\.)", file_name)
            if m :
                file_sequence_padding = m.group()
                pad_length = len(file_sequence_padding)
                ffpmeg_input = file_name.replace(file_sequence_padding, 
                                f'%0{pad_length}d')
                return str(img_start.parent / ffpmeg_input)

    @staticmethod
    def playblast_output_to_ffmpeg_input(img: str) -> str:
        """
            Takes an image input path, and calculates the padding via regex. 
            Then replaces this file numbering with an ffmpeg compliant string. 

            Similar to above, I wanted a method that handled maya playblasts 
            specifically.

        Args:
            img (str): Str object of a hashed file sequence
            This is for the return string from a Maya playblast

        Returns:
            str: A new, formated path string containing the 
                ffmpeg padding characters.
        """
        if img:
            # if name matches a regex pattern with a number of digits
            m = re.search(r"(\#{3,})", img)
            if m :
                file_sequence_padding = m.group()
                pad_length = len(file_sequence_padding)
                ffpmeg_input = img.replace(file_sequence_padding, 
                                f'%0{pad_length}d')
                return str(ffpmeg_input)

    @staticmethod

    def create_ffmpeg_still_frame_output(input_file: str, 
                                   filename: str, 
                                   padding: int = 4, 
                                   ext: str = '.png'
                                   ) -> str:
        """
        Create a filename for ffmpeg still frame output.

        Args: 
            input_file (str): the input file to create the filename for.
            filename (str): the filename to use.
            padding (int):the padding to use.
            ext (str): the extension to use. Defaults to ".png"
        
        returns:
            str: the filename for ffmpeg still frame output.
        """
        image_root = Path(input_file)

        if not ext.startswith('.'):
            ext = f'.{ext}'

        if image_root.exists():
            filename = f'{image_root.stem}_%0{padding}d{ext}'
            return image_root.parent / filename

class FolderOps:  
    """
    Static class containing useful file operations
    """  
    
    VERSION_STR :str = 'v'
    VERSION_DEFAULT:str = f'{VERSION_STR}{1:03d}'
    EXTENSION_DEFAULT:str = '.png'

    @staticmethod
    def explore(dir:str) -> bool:
        """
        `explore` takes a directory name as a string and returns a boolean
        
        Args:
          dir (str): The directory to explore

        Returns:
            bool: if successful
        """
        
        subprocess.Popen(f'explorer  "{dir}"')

    @staticmethod
    def purge_contents( root:str,  
                        ext: str = '.*',
                        skip_folder: str = ""
                        ):
        """Removes files from the directory. 
            Designed to be used in 2 ways :
            1. Remove everything 
            2. Remove a filetype (pass an extension to target)
            3. If you want to keep capture images, pass the folder name

        Args:
            root (str): The base path to scan for files
            ext (str, optional): The extension to remove. Defaults to '.*'.
            skip_folder (str, optional): Folder name to skip. Defaults to "".
        """
        for f in Path(root).rglob(f'*{ext}'):
            try:
                if f.parent.name != skip_folder:
                    f.unlink()
            except OSError as e:
                print(f"Error:{f} : {e.strerror}")

    @classmethod
    def get_version_folders(cls, rootDir: str, 
                            latest: bool = True
                            ) -> Union[str,None]:
        """Gets the last version folder in a directory, or a list of versions if 
        latest is set to false.

        Args:
            rootDir (str): The root directory as a string
            latest (bool, optional): Returns a string of the last version
                                     folder found. Defaults to True.

        Returns:
            Union[str,None]: Returns the version folder string or none if no
                             folders are found. This version string can then 
                             be used with FolderUtils.nextVersion()

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
    def next_version(cls, vStr: str ) -> str:
        """Takes a version string and returns the next version 
           as a string - e.g. 'v005' returns 'v006'.

        Args:
            vStr (str): The version number (from a folder name)

        Returns:
            str: the next incremental version string
        """
        if vStr!= None:
            vNumber =  vStr.lstrip('v')
            vInt = int(vNumber)
            vInt +=1
            return f'v{vInt:03d}'
        else:
            return cls.VERSION_DEFAULT


    @classmethod
    def getImageSequence(cls, dir: str, ext:str=None) -> Path:
        """
        Looked into being able to glob multiple filetpyes, then decided after 
        the code looked confusing as you'll always set the format in the Maya 
        playblast. This is a simple glob call via Pathlib. 

        Args:
            dir (str): Root directory of the file sequence 
            ext (str, optional): the image file extension. Defaults to 'png'.

        Returns:
            Path: The first image in the found sequence

        This function is depreciated and will be removed
        """
        if not ext:
            ext = cls.EXTENSION_DEFAULT

        dirPath = Path(dir)
        if dirPath.exists():
            sequence = dirPath.glob(f'*{ext}')  
            return next(sequence)
        

    @classmethod
    def get_first_frame_from_filename(cls, dir: str, ext:str=None) -> Path:
        """
        Looked into being able to glob multiple filetpyes, then decided after 
        the code looked confusing as you'll always set the format in the Maya 
        playblast. This is a simple glob call via Pathlib. 

        Args:
            dir (str): Root directory of the file sequence 
            ext (str, optional): the image file extension. Defaults to 'png'.

        Returns:
            Path: The first image in the found sequence

        This function is depreciated and will be removed
        """
        if not ext:
            ext = cls.EXTENSION_DEFAULT

        dirPath = Path(dir)
        print (dirPath.parent)
        if dirPath.parent.exists():
            sequence = dirPath.glob(f'*{ext}')  
            print (f' sequence {next(sequence)}')
            return next(sequence)
        
        

