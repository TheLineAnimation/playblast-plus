"""
Base class for the methods applicable to each host
"""
class PreviewRender():

    def create(self, **kwargs) -> str:
        pass

    def snapshot(self,**kwargs):
        pass

    def pre_process(self,**kwargs):
        pass

    def post_process(self,**kwargs):
        pass

    def set_override_properties(self,**kwargs) -> dict:
        pass

    def notify_user(self, message):
        pass
