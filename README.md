### Playblasting in 3d DCCs so it doesn't completely suck

<img align="right" src="https://theline.imgix.net/Toban_still_16-9_000010.png"/>

<br>

Let's face it, Maya's playblast isn't the best. (And that's saying something as a long-time 3dsmax user)
This script standardizes the playblast output to allow animators an easy way to create a rolling,
local playblast to review their work. 

<br>

### Why bother? 

As an animator, you don't always want to submit a playblast for project review. 
There might be a number of iterations you need to perform before you are 
ready to let those keyframes fly, like little tweened starlings flocking in an animated sky.

Playblast Plus is in debt to the great coding work from the following sources - 

- [maya-capture](https://github.com/abstractfactory/maya-capture). 
    The core module is being used as is, and contains pretty much all the playblasting functionality you'd need. Current version - 2.1.0

- [maya-capture-gui](https://github.com/BigRoy/maya-capture-gui) by Roy Nieterau
    Used the tokenized string parsing from this repo, as this is a very nice way of performing function based string substitution. 

- [Qt.py](https://github.com/mottosso/Qt.py)
    Minimal Python 2 & 3 shim around all Qt bindings - PySide, PySide2, PyQt4 and PyQt5.

- [Chris-Zurbrig](https://zurbrigg.com) 
    Chris's FFMPEG in production course was the starting point for the FFMPEG encoding part of the script. Maya's codec support is woeful and this wouldn't be possible without it. Updated the examples to utilise the new f-string formatting in Python 3

- [Jerome Dresse](http://www.nodilus.lu) 
    Jerome's Smear Deformer script has a great UI that I was able to re-task as the basis of the qt ui. 

So this is more of a Dr.Frankenstein script, made from parts created by people who can actually code. Thanks to everyone listed here for sharing their knowledge.  

<br>

### Documentation

- [Click here for detailed documentation](https://thelineanimation.github.io/playblast-plus/) about usage, installation and the python class descriptions

You can also click the header in the UI to launch this help inside your DCC. 

<img align="center" src="https://github.com/TheLineAnimation/playblast-plus/blob/main/docs/_images/ui.png?raw=true"/>

<br>

### Features

- Transcodes the Maya playblast into MP4 (Uses [FFMpeg](https://ffmpeg.org/))
- Template overrides for common requirements, like show wireframe and image planes
- Tokenized path output to control filenames and paths.

<br>

### How it all works

- Code base runs from a networked location, and offloads the transcoding to the local machine
- playblasts/previews and captures reside on the artist's machine
- requires FFMpeg to be installed locally. The location isn't important and can be configured to multiple folders globally to allow different setups. 

<img align="right" src="https://github.com/TheLineAnimation/playblast-plus/blob/main/docs/_images/pbp_structure.png?raw=true"/>

<br>

### Installation

To install, download this and place the PlayblastPlus folder in a directory on your PYTHONPATH

<br>

### Usage

To show the interface in any supported host, run:

```python
import playblast_plus.launch
playblast_plus.launch.run()
```

<br>

### To-Do

- Tidy up the project template idea, feels redundant now.


