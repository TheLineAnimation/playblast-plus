=========================
Playblast Plus |version|
=========================

Playblast Plus is a python library that is designed to facilitate animation workflows with consistent,
yet customisable content previews in a variety of DDC Hosts. 

.. _ui:

.. figure:: /images/ui.png
  :width: 18em
  :align: center

  The main interface

.. admonition:: The Problem
    :class: warning

    Both Maya and 3dsMax have pretty awful ways to create quick animation previews. 
    They aren't particularly sharable and animation sequences have very sketchy codec support. 

Playblast Plus solves this by...
-----------------------------------

- Using the host's native preview functionality to render a frame sequence, parsing it to ffMpeg to render a H264 MP4 file. This allows animators to see their work more often and spend less time rendering viewable previews. 
- Applying a view template to the preview so that you can define a set appearance to previews, making sure different animators create reviews with identical visual settings.
- Giving flexibility to override some parameters, like image planes (backgrounds), wireframe renders and isolating key components.
- Providing both animation preview and viewport image capture.
