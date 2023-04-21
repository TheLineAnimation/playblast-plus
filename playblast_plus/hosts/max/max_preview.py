from ...lib import preview
from ...lib import utils
from pathlib import Path

from pymxs import runtime as mxs 
import qtmax

# qtmax.DisableMaxAcceleratorsOnFocus(self, True)

""" 
    createPreview 
        filename:<string> 
        outputAVI:<boolean> 
        percentSize:<int> \
        start:<int> 
        end:<int> 
        skip:<int> 
        fps:<int> \
        dspGeometry:<boolean> 
        dspShapes:<boolean> 
        dspLights:<boolean> \
        dspCameras:<boolean> 
        dspHelpers:<boolean> 
        dspSpaceWarps:<boolean> 
        dspParticles:<boolean> \
        dspBones:<boolean> 
        dspGrid:<boolean> 
        dspSafeFrame:<boolean> 
        dspFrameNums:<boolean> \ 
        dspBkg:<boolean> 
        rndLevel:<#smoothhighlights | #smooth | #facethighlights \ 
        | #facet | #flat | #hiddenline | #litwireframe | #wireframe | #box> \
        useMPCamEffect:<boolean> 
        snippet:<string>
"""

class MakePreview(preview.PreviewRender):

    def create(self, **kwargs) -> str:

        """
        https://cganimator.com/uiaccessor-mini-tutorial-how-to-control-make-preview-dialog/
        """
        
        # mxs.CreatePreview()

        template = kwargs['template']
        host_options = kwargs['host_options']
     
        wireframe_option = template['viewport_options']['wireframeOnShaded']
        half_res_option = host_options['set_half']

        # isolate_option = template['isolate_option']
        image_plane_option = template['viewport_options']['imagePlane']
        # override_layer_name = template['override_layer_name']

        template = kwargs['template']

        if half_res_option:
            percentSize=50
        else:
            percentSize=100 

        filename = template['filename']
        ext = template['compression']
        output_filename =  f'{filename}_.{ext}'

        print (f'output_filename create func {output_filename}')

        mxs.createPreview (
            filename=output_filename, 
            outputAVI=False, 
            percentSize=percentSize,
            start=mxs.animationRange.start,
            end=mxs.animationRange.end,
            fps=int(mxs.currentTime), 
            dspGeometry=True, 
            dspShapes=False,
            dspLights=False,
            dspCameras=False,
            dspHelpers=False,
            dspSpaceWarps=False,
            dspParticles=False,
            dspBones=False,
            dspGrid=False,
            dspSafeFrame=False,
            dspFrameNums=False,
            dspBkg=image_plane_option
            )
        
        preview_file = Path(output_filename)
        
        sequence = preview_file.parent.glob(f'{preview_file.stem}*{ext}')

        if sequence:
            first_frame = next(sequence)
            ffmpeg_input = utils.Parsing.create_ffmpeg_input(first_frame)
            print (f'create func ffmpeg_input_string {ffmpeg_input}')
            return ffmpeg_input


    def snapshot(self,**kwargs):

        template = kwargs['template']
        # host_options = kwargs['host_options']

        filename = template['filename']
        ct = str(int(mxs.currentTime)).zfill(4)
        ext = template['compression']

        viewport_bitmap = mxs.viewport.getViewportDib(captureAlpha=True)
        viewport_bitmap.filename =  f'{filename}_{ct}.{ext}'

        print (f'snapshot func {viewport_bitmap.filename}')
        mxs.display(viewport_bitmap)
        mxs.save(viewport_bitmap)

        print (f'snapshot func {kwargs}')

    def pre_process(self,**kwargs):
        # wireframe_option = kwargs['set_wire']
        # mxs.viewport.SetShowEdgeFaces(wireframe_option)

       # set up isolate set - select isolate selected, deselect  
        print (f'pre process func {kwargs}')

    def post_process(self,**kwargs):
        wireframe_option = kwargs['wireframe_option']
        if wireframe_option:
            mxs.viewport.SetShowEdgeFaces(False)

         # revert isolate set - unisolate mode
        
        print (f'post process func {kwargs}')
    
    def set_override_properties(self,**kwargs) -> dict:

        """
        mxs.viewport.SetShowEdgeFaces(True)
        print (mxs.viewport.GetShowEdgeFaces())
        """
        print (f'set override properties func {kwargs}')

        wireframe_option = kwargs['wireframe_option']
        mxs.viewport.SetShowEdgeFaces(wireframe_option)


    def notify_user(self, message):
        mxs.pushPrompt(message)

