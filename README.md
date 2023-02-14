### Playblasting in Maya that doesn't completely suck


Let's face it, Maya's playblast isn't the best. (And that's saying something as a long-time 3dsmax user)
This script standardises the playblast output to allow animators an easy way to create a rolling,
local playblast to review thier work. 

<img align="right" src="https://theline.imgix.net/Toban_still_16-9_000010.png"/>

<br>

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

- Transcodes the Maya playblast into MP4 (Uses [FFMpeg](https://ffmpeg.org/))
- Template overrides for common requirements, like show wireframe and image planes
- Tokenized path output to control filenames and paths.

<br>

### Installation

To install, download this and place the PlayblastPlus folder in a directory on your PYTHONPATH

<br>

### Usage

To show the interface in Maya run:

```python
import playblast_plus.ui
playblast_plus.ui.run()
```

<br>

### To-Do

- Tidy up the project template idea, feels redundant now.

### Known issues
