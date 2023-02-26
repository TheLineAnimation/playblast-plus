Playblast Template
-------------------

To explain how the system works, we have to look at the building block - the script template. 

The template contains a JSON dictionary and the keys in this are loaded as a representation of the parameters the script needs 
to be displayed and executed in the host.

.. code-block:: json

   {
      "scriptName": "ExampleScript",
      "niceName": "Example Script",
      "version": 1.1,
      "modifiedDate": "2022-06-17",
      "exec": true,
      "project":false,
      "host": "maya",
      "task":"anim.camera.color.light.model.pipeline.render.rig.shade.tools",
      "language":"python",
      "type": "script",
      "modulePath":"studio.core.*",
      "tags":[
         "anim",
         "animation",
         "bake",
         "key",
         "keyframe",
         "track",
         "pointtrack"
      ],
      "quickhelp":"A script to do blah blah blah",
      "command":"print (sys.path)",
      "runcount": 0
   }

A script requires the following parameters to be set in order to be located and executed in the correct way. 

