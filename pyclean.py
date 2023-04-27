""" 
Script to run from the terminal to clean up python caches ahead of release
"""

import pathlib

[p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]
[p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]