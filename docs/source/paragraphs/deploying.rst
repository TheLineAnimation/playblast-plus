
Deploying Playblast Plus
---------------------------

Playblast Plus can run in two different ways : 

- Completely localised on an artist's workstation.
- From a network location to allow Pipeline TDs to specify versions and allow for easy updates in a Studio setting

This is because it only runs the core code from the library and offloads any transcoding to a local install of MMPeg. 


Environment
------------

Studio Pipeline has been designed to run with the minimum amount of setup.
It requires the directory to be visible on the PYTHONPATH, and this can be set 
identivally for multiple hosts.

PBP is executed via a launch.py script, which detects the host executable 
and imports the relevant DCC-centrict modules.

.. code:: python
    
    PYTHONPATH = {STUDIOPIPELINE_VERSION_FOLDER}/hosts/maya

Running from a networked drive is the prefered route for a Studio install, as the
PYTHONPATH environment varibale can be set via something like Active directory or within a pipeline loder, like OpenPype/Ayon.

Pipeline Versions
-----------------

