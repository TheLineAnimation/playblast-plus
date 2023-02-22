import sys
from pathlib import Path

class Host():
    @classmethod
    def get_name(cls) -> str:
        host_exe = cls.get_executable()
        return ( str(host_exe.stem ))
    @classmethod
    def get_executable(cls) -> Path:
        return Path(sys.executable)

    