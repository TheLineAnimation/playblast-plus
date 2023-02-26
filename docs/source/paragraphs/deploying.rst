
Deploying Playblast Plus
---------------------------

Studio Pipeline could be easily deployed outside of a formal pipeline, but given we operate inside the Open Pype ecosystem, 
it is best invoked within the open pype envirnoment. Open Pype has a concept of tools that can be versioned and deployed on a project by project basis.
It also allows for changes to be made depending on software version, as each project can be configured to run a particular version. 

Environment
------------

Studio Pipeline has been designed to run with the minimum amount of setup.

.. code:: python
    
    MAYA_MODULE_PATH = {STUDIOPIPELINE_VERSION_FOLDER}/hosts/maya


Pipeline Versions
-----------------

Additionally, different versions of the Pipeline can be hosted and run according to the version number. This version number becomes part of the load path so the host can look for the version compatible with it. New versions can be cloned and developed, leaving production tested (and working code) untouched and running in that particular host version.


