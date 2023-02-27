
class Scene():
    """
    Base class for each host to inherit methods for preview handling
    """

    @staticmethod
    def main_window():
        pass



    @staticmethod
    def get_name():
        """
        Returns the scene file name
        """
        pass

    @staticmethod
    def get_scene_cameras():
        """Returns the scene cameras, surprisingly
        """
        pass
    
    @staticmethod
    def get_current_camera():
        """Returns the currently active camera.

        Returns:
            str: name of active camera transform
        """

        pass

    @staticmethod
    # maybe use *args here for different hosts             
    def get_output_dir(*args) -> str:
        """Returns the playblast directory so that a filename can be specified.

        Args:
            workspace (bool, optional): Decides if the playblast is local to the 
            Host install or the workspace location. Defaults to False.

        Returns:
            string: A folder location string
        """

        pass

