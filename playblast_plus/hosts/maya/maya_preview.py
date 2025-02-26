from ...lib import preview
from ...lib import utils

import maya.cmds as cmds
from maya import OpenMaya, OpenMayaUI

# Import Shiboken with fallback
try:
    from shiboken6 import wrapInstance
except ImportError:
    try:
        from shiboken2 import wrapInstance
    except ImportError:
        raise ImportError("Neither shiboken6 nor shiboken2 could be imported. Please install one of them.")

from ...hosts.maya import capture
from ...hosts.maya import register_tokens

# from pathlib import Path

class Playblast(preview.PreviewRender):

    def create(self, **kwargs) -> str:
        """
        template only is needed????? 
       
        """
        if kwargs['template']:
            filename = capture.capture(**kwargs['template'])
            ffmpeg_input_string = \
                utils.Parsing.playblast_output_to_ffmpeg_input(filename)
            return ffmpeg_input_string

    def snapshot(self,**kwargs):

        if kwargs['template']:
            filename = capture.snap(**kwargs['template'])
            return filename

    def pre_process(self,**kwargs):
        isolate_set_name = kwargs['isolate_set_name']

        if not cmds.ls(isolate_set_name, sets=True):
            cmds.sets(name=isolate_set_name, empty=True)

        # add a check for the gpucache plugin, as this can create an 
        # issue with the plugin filter not being detected and the tempate 
        # throwing an error
        if not cmds.pluginInfo('gpuCache',q=True,l=True):    
            result = cmds.confirmDialog( title='Playblast Plus',
                                message='Playblast Plus has detected that the GPUCache is disabled. Click Ok to enable it and use without issues.', 
                                button=['Ok','Nope'], 
                                defaultButton='Yes', 
                                cancelButton='Nope', 
                                dismissString='Nope' )
            if result == 'Ok':                    
                try: 
                    cmds.loadPlugin('gpuCache')
                except: 
                    raise Exception('Unable to load gpuCache plugin!')
            elif result == 'Nope':
                self.notify_user("You need to enable the GPU Cache for this script to work correctly.")
 
    def post_process(self,**kwargs):
        wireframe_option = kwargs['wireframe_option'] 
        override_layer_name = kwargs['override_layer_name'] 
    
        if wireframe_option:
            try:
                cmds.delete(override_layer_name)
            except:
                self.notify_user(
                    f'Something went wrong deleting the display layer'
                    '- {override_layer_name}')

    def notify_user(self, message):
        if message:
            cmds.inViewMessage( message=message,
                        fade=True, position="midCenter", fontSize=16,
                        fadeStayTime=1000, fadeOutTime=100,
                        dragKill=True, bkc=0x00154060, alpha=0.7)


    def kill(self,**kwargs):
        """ Deletes an already created widget

        Args:
            name (str): the widget object name
        """
        name = kwargs['name']

        # finds workspace control if dockable widget
        if cmds.workspaceControl(name, exists=True):
            cmds.workspaceControl(name, edit=True, clp=False)
            cmds.deleteUI(name)

        # finds the widget
        widget = OpenMayaUI.MQtUtil.findWindow(name)
        return widget
        # if not widget:
        #     return

        # # wraps the widget into a qt object
        # qt_object = wrapInstance(long(widget), QtWidgets.QDialog)
        # # sets the widget parent to none
        # qt_object.setParent(None)

        # # deletes the widget
        # qt_object.deleteLater()
        # del(qt_object)

    def set_override_properties(self,**kwargs) -> dict:
        """
        Add all objects to display layer and set to black, then remove afterwards
        """
        template_override_setting = kwargs['template_override_setting']
        wireframe_option = kwargs['wireframe_option']
        half_res_option = kwargs['half_res_option']
        isolate_option = kwargs['isolate_option']
        image_plane_option = kwargs['image_plane_option']
        override_layer_name = kwargs['override_layer_name']
        wireframe_color = kwargs['wireframe_color']
        render_width = kwargs['render_width']
        render_height = kwargs['render_height']
        template = kwargs['template']

        viewport = cmds.getPanel( withFocus=True)
        if template_override_setting: 
            # is wireframe override on? 
            wf_override_state = wireframe_option
            template["viewport_options"]["wireframeOnShaded"] = wf_override_state
            
            if wf_override_state:
                if override_layer_name in cmds.ls(typ='displayLayer'):
                    cmds.delete(override_layer_name)

                geo = cmds.listRelatives(cmds.ls(geometry=True), p=True, path=True)
                wfGroup = cmds.createDisplayLayer(geo, n=override_layer_name)
                wf_col = wireframe_color
                cmds.setAttr("{}.color".format(wfGroup), True)
                cmds.setAttr("{}.overrideRGBColors".format(wfGroup), True)
                cmds.setAttr("{}.overrideColorRGB".format(wfGroup), wf_col[0], wf_col[1], wf_col[2])
            
            if 'modelPanel' in viewport:
                cmds.modelEditor(viewport, 
                                 edit=True, 
                                 wireframeOnShaded=wf_override_state)

            template["viewport_options"]["imagePlane"] = image_plane_option

            if half_res_option:
            #    calculate the current res and halve it
                # width, height = scene.get_render_resolution(0.5)
                template["width"] = render_width
                template["height"] = render_height
                # PlayBlastPlusLogger.info(f'New Playblast Size {width}x{height}')

            if isolate_option:
                if cmds.ls("pbp_isolate", sets=True):
                    isolate_nodes = cmds.sets('pbp_isolate', q = True)
                    template["isolate"] = isolate_nodes

        else:
            if 'modelPanel' in viewport:
                cmds.modelEditor(viewport, edit=True, wireframeOnShaded=False)
        print (f'TEMPLATE FROM PREVIEW {template}')

        return template

