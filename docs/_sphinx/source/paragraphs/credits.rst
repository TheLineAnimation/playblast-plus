===================
Credits and Thanks
===================

I used the following resources to build Playblast Plus:

- `Chris Zurbrigg <https://zurbrigg.com/courses>`_'s teaching resources - Chris has an in-depth python series specific to Maya (Plus a great tool with an enhanced featureset - `Advanced Playblast <https://zurbrigg.com/advanced-playblast>`_ )
- `Maya Capture <https://github.com/abstractfactory/maya-capture>`_ - By - A very capable playblast library that encapsulates the preset functionality
- `Maya Capture GUI <https://github.com/BigRoy/maya-capture-gui>`_ - By Roy Nietereau - Was a helpful git repo that had the token system used in the dynamic filename creation
- `Jerome Dresse <https://www.nodilus.lu/>`_ - A superstar technical director, and provider of the code I used as a template for the user interface
- `Qt.py <https://github.com/mottosso/Qt.py>` - Minimal Python 2 & 3 shim around all Qt bindings - PySide, PySide2, PyQt4 and PyQt5.

===============================
Technical Documentation
===============================
    .. container:: tocdescr

      .. container:: descr
         ..name templates

         .. figure:: /images/studio_ui.jpg
            :target: ./paragraphs/templates.html

         Templates
            Overview of how the template system works in Playblast Plus

      .. container:: descr
         ..name python

         .. figure:: /images/studio_ui.jpg
            :target: ./paragraphs/python.html

         Python Documentation
            Auto-generated documentation for the codebase

.. admonition:: Known Issues
    :class: warning

    - Maya is a bit cranky in returning the camera from the viewport. I need to find a better way to return the active viewport's camera name from the token system, or provide a fallback
    - Catch if the half res option results in an odd number for the W or H resolution. Otherwise ffMpeg will thow an error.  

.. admonition:: Future Development
    :class: hint

    - Given this has capability to deliver a Host-centric solution for previewing - it should have the framework to function in more hosts than Maya and 3dsMax. 
    - Nuke would be potentially viable - instead of cameras, it could execute write nodes inside the current nuke script. 
    - Blender might be more problematic to run via the same UI, but it could have a custom operator in this specific case and still utilise all the core classes for encoding.

