
class Scene():
    """
    Base class for each host to inherit methods for preview handling
    """
    @staticmethod
    def main_window():
        """Retrieves the main_window handle of the DCC.

        Returns:
            ptr: A pointer to the window object
        """
        pass

    @staticmethod
    def get_name():
        """
        Returns:
            str: The scene file name
        """
        pass

    @staticmethod
    def get_scene_cameras():
        """
        Returns:
            str: Returns the scene cameras, surprisingly
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
    def get_active_sound(start_frame: float = 0.0):
        """Returns the scene sound to include in the preview, if any.

        Returns:
            tuple|None: (audio_file_path, audio_seconds_at_start_frame) or None
        """
        return None

    @staticmethod
    def get_focal_lengths(camera, start_frame, end_frame):
        """Per-frame camera focal length in mm, or None if not supported."""
        return None

    @staticmethod
    def get_burnin_context() -> dict:
        """Context values for the burnin (folder name, workfile version)."""
        return {'folder': '', 'version': ''}

    @staticmethod
    # maybe use *args here for different hosts
    def get_output_dir(*args) -> str:
        """Returns the playblast directory so that a filename can be specified.

        Args:
            workspace (bool, optional): Decides if the playblast is local to the 
            Host install or the workspace location. Defaults to False.

        Returns:
            str: A folder location string
        """

        pass

