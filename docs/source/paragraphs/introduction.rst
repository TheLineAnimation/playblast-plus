================
Playblast Plus
================

Playblast Plus is a python library that is designed to facilitate animation workflows with consistent,
yet customisable content previews in a variety of DDC Hosts. 

The Problem - Both Maya, 3dsMax, Nuke all have pretty awful ways to create quick previews. 
They aren't particulary sharable and animation sequences have very sketchy codec support. 

Playblast Plus solves this by using the host's native preview functionality to render a frame sequence,
and then passes it to FFMpeg to render a H264 MP4 fie. This allows animators to see their wor more often
and spend less time rendering viewable previews. 

