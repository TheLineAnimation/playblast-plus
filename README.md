### Playblasting in Maya that doesn't completely suck


Let's face it, Maya's playblast isn't the best. (And that's saying something as a long-time 3dsmax user)
This script standardises the playblast output to allow animators an easy way to create a rolling,
local playblast to review thier work. 

Compatible with the OpenPype reiew workflow - specifically the `review` instance to ensure settings parity, 
but allow custom preview settings on a local level.

<img align="right" src="https://theline.imgix.net/Toban_still_16-9_000010.png"/>


### Why bother? 

As an animator, you don't always want to submit a playblast for project review. 
There might be a number of iterations you need to perform before you are 
ready to let those keyframes fly, like little tweened starlings flocking in an animated sky.

Playblast Plus is in debt to the great coding work from the following sources - 

- [maya-capture](https://github.com/abstractfactory/maya-capture). The core module is being used as is, 
    and contains pretty much all the playblasting functionality you'd need. Current version - 2.1.0

- [maya-capture-gui]() by Roy Nieterau (Colorbleed)
    I could have used Big Roy's front-end, but I wanted to at least try to learn something for myself. Used the tokenised string parsing, this is a very elegant way of performing function based string substituation. 

- [Chris-Zurbrig]() Chris's FFMPEG in production course is responsible for the FFMPEG encoding of the
    script. Maya's codec support is woeful and this wouldn't be possible without it. 

So this is more of a Dr.Frankenstein script, made from parts created by people who can actually code. It makes a change from a Dr.Franenstein script created by Stack Overflow. 

<br>

### Features

- Configurable viewport settings to switch between different preview settings 
- Tokenized path output to control filenames and paths without the need to set one.
- Callbacks to allow custom encoding prior to opening viewer.
- Configure project override templates to allow alternate options (like wireframe previews and snapshots) 
- Utilises [OpenPype](https://openpype.io) environment

<br>

### Installation

To install, download this and place the PlayblastPlus folder in a directory on your PYTHONPATH

<br>

### Usage (WIP but keeping the MD formatting stuff for later)

To show the interface in Maya run:

```python
import playblast_plus
capture_gui.main()
```

<br>

### Advanced

#### Callbacks
Register a pre-view callback to allow a custom conversion or overlays on the 
resulting footage in your pipeline (e.g. through FFMPEG)

```python
import capture_gui

# Use Qt.py to be both compatible with PySide and PySide2 (Maya 2017+)
from capture_gui.vendor.Qt import QtCore

def callback(options):
    """Implement your callback here"""

    print("Callback before launching viewer..")

    # Debug print all options for example purposes
    import pprint
    pprint.pprint(options)

    filename = options['filename']
    print("Finished callback for video {0}".format(filename))


app = capture_gui.main(show=False)

# Use QtCore.Qt.DirectConnection to ensure the viewer waits to launch until
# your callback has finished. This is especially important when using your
# callback to perform an extra encoding pass over the resulting file.
app.viewer_start.connect(callback, QtCore.Qt.DirectConnection)

# Show the app manually
app.show()
```

#### Register preset paths

Register a preset path that will be used by the capture gui to load default presets from.

```python
import capture_gui.presets
import capture_gui

path = "path/to/directory"
capture_gui.presets.register_path(path)

# After registering capture gui will automatically load
# the presets found in all registered preset paths
capture_gui.main()
```

#### Register tokens and translators

Register a token and translator that will be used to translate any tokens
in the given filename.

```python
import capture.tokens
import capture_gui

# this is an example function which retrieves the name of the current user
def get_user_name():
    import getpass
    return getpass.getuser()

# register the token <User> and pass the function which should be called
# when this token is present.
# The label is for the right mouse button menu's readability.
capture.tokens.register_token("<User>",
                              lambda options : get_user_name(),
                              label="Insert current user's name")
```

### Known issues
