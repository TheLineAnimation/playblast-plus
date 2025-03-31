"""
  _____ _  _ ___   _	___ _  _ ___			
 |_   _| || | __| | |  |_ _| \| | __|   		
_______________________________________          
   |_| |_||_|___| |____|___|_|\_|___|   		
                                                
    _   _  _ ___ __  __   _ _____ ___ ___  _  _ 
   /_\ | \| |_ _|  \/  | /_\_   _|_ _/ _ \| \| |
  / _ \| .` || || |\/| |/ _ \| |  | | (_) | .` |
 /_/ \_\_|\_|___|_|  |_/_/ \_\_| |___\___/|_|\_|
 
PLAYBLAST PLUS

pete@thelineanimation.com

"""
VERSION_MAJOR = 1
VERSION_MINOR = 5
VERSION_PATCH = 0

version_info = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
version = '%i.%i.%i' % version_info
__version__ = version

__all__ = ['version', 'version_info', '__version__']

