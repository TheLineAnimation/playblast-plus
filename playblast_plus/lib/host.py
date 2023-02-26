import sys
from pathlib import Path

class Host():
    """_summary_

    Returns:
        _type_: _description_
    """
    @classmethod
    def get_name(cls) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        host_exe = cls.get_executable()
        return ( str( host_exe.stem ))
    @classmethod
    def get_executable(cls) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        return Path(sys.executable)

    