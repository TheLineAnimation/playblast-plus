
Deploying Playblast Plus
---------------------------

Playblast Plus can run in two different ways : 

- Completely localised on an artist's workstation.
- From a network location to allow Pipeline TDs to specify versions and allow for easy updates in a studio setting

This is because it only runs the core code from the library and offloads any transcoding to a local install of ffMpeg. 

Setup Module Environment
-------------------------

Playblast Plus requires the directory to be visible on the PYTHONPATH, and this can be set identically for multiple hosts.

.. important::
    **Playblast Plus is Python 3x only.**

    I decided that given the minimum DCC version used in future productions wouldn't be anything before the 2022 releases, I decided it's too much to support older host versions. I thought about this **a lot** and decided Python 2 support needed to go. Python 3 is the future. 

.. code:: python
    
    PYTHONPATH = {PLAYBLAST PLUS FOLDER}

Running from a networked drive is the prefered route for a Studio install, as the PYTHONPATH environment varibale can be set via something like Active directory, or within a pipeline loder like OpenPype/Ayon.
You could keep the `playblast plus` folder marked with the version release. This way, you would have a flexxible way to update and test new versions, as you can point the python path at the specific version for each DCC version

Launching the UI
------------------

This should be an identical call regardless of host. Playblast Plus is executed via a launch.py script, which detects the host executable and imports the relevant DCC-centrict modules.

.. code:: python

    from playblast_plus import launch
    launch.run()

Setting up ffMpeg 
---------------------------

Playblast plus uses ffMpeg to transcode the preview image sequences into a H264 encoded MP4. It does this seamlessly after the preiew stage, but you need to have the executable located somewhere on your local system. 

I don't bundle the executable with the code base for a number of reasons, but the main one is so that the encoding step is offloaded to the local machine, while the main codebase can be run from a network. Whilst Playblast Plus will work fine when installed locally, run from a netwrok means the studio template default is applied across the board, and any changes to this will be adopted studio-wide automatically.

.. _download_picture:

.. figure:: /images/downloader.gif
  :width: 24em
  :align: center

  The downloader interface

Playblast Plus will search any locations that are present in the `config.json` and look for `ffMpeg.exe`. If it doesn't find any, it will present you with a downloader to do this. 

This will download the ffMpeg version specified in the config key `ffmpeg:download_url` to the current user directory. Simply unpack the zip and drop ffMpeg.exe into one of the locations shown, or install to a folder of your choice and update `config.json` to include this path.

.. tip::
    if you don't alter the first entry of the `executable_paths` entry, it will resolve a relative folder called **/bin** in the current script environment.

I don't unpack and move this automtically, I decided it's ok for someone to decide where they run this from.

Understanding the config.json
-------------------------------

Playblast Plus will take core settings from the `config.json` located in the root folder of the module. This contains data that informs the main operation of the module. 

.. code-block:: json
    {
        "studio_templates": "./templates/studio",
        "project_template_subpath": "tools/pipeline/playblast/templates",
        "documentation_url":"https://thelineanimation.com",
        "overrides": {
        "wireframe_color": [0.1,0.1,0.1]
        },
        "default_output_token": "<scene>_<user>",
        "ffmpeg": {
            "download_url":"https://github.com/GyanD/codexffmpeg/releases/download/5.1.2/ffmpeg-5.1.2-essentials_build.zip",
            "executable_paths": [
                "./bin",
                "C:/Program Files/ffmpeg/bin"
                ],
            "input_args": "-c:v libx264 -crf 21 -preset ultrafast -pix_fmt yuv420p",
            "output_args": "",
            "burnin": {
                "enabled":true,
                "prefix_text": ""
            }
        }
    }

Adding this to a shelf in Maya
--------------------------------

Adding this to a menu/quad in 3dsMax
--------------------------------------
