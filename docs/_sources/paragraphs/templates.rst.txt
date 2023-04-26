Playblast Template
-------------------

To explain how the system works, we have to look at the core block - the capture template. 

The template contains a JSON dictionary and the keys in this are properties to setup the viewport to render the preview. 

.. code-block:: json

   {
      "overwrite": true ,
      "show_ornaments": false,
      "off_screen":true, 
      "filename": "playblast",
      "compression": "png", 
      "format": "image", 
      "viewer": false,
      "frame_padding":4,
      "maintain_aspect_ratio":true,
      "quality":100,
      "display_options": {
         "displayGradient": false,
         "background": [
               0.36000001430511475,
               0.36000001430511475,
               0.36000001430511475
         ],
         "backgroundTop": [
               0.5350000262260437,
               0.6169999837875366,
               0.7020000219345093
         ],
         "backgroundBottom": [
               0.052000001072883606,
               0.052000001072883606,
               0.052000001072883606
         ]
      },
      "camera_options": {
         "displayGateMask": false,
         "displayResolution": false,
         "displayFilmGate": false,
         "displayFieldChart": false,
         "displaySafeAction": false,
         "displaySafeTitle": false,
         "displayFilmPivot": false,
         "displayFilmOrigin": false,
         "overscan": 1.0,
         "depthOfField": false
      }
   }

This is an excerpt of the full template. You can create multiple clones of this and adjust settings according to your needs. If you need to do this, it's highly likely that you will know what these setting will mean. 

Maya Capture vs 3dsMax preview
--------------------------------

Given we use Maya capture as the template for previewing, the main question is *how does this work when the DCC and the terminology is different?* For 3dsmax, there's clearly enough overlap in concepts to be able to handle many of the key areas of how Maya performs a playblast. Given the function calls are specific, each host can parse and implement the settings however it likes. 
