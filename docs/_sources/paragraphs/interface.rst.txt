
Using Playblast Plus
=====================

.. _ui_sections:

.. figure:: /images/ui_sections.png
  :width: 18em
  :align: center

  The main interface

  The main ui consists of the following areas - 

**1. Settings Menu** 
  Where you customise the behaviour of the script (See below for details)
**2. The template dropdown** 
  Where you can select the preview preset template
**3. Template Overrides** 
  Some common overrides that can be applied (rather than having to create a new template)
**4. Output Name** 
  A text box to specify the output name (See Tokenised Output)
**5. Camera Dropdown** 
  A list of the cameras in the scene. In the Maya host, it won't list any startup cameras (The 4 main views)
  Picking an item fro this list will decide what camera is previewed, irrespective of the active view.
**6. Capture Buttons**
  There are two options and the button text will vary depending on the host (Playblast in Maya, Preview in 3dsmax)
  Playblast executes a playblast to the current time slider range, and Snap will snapshot the selected view. Any template overrides will be applied to the playblast and the view snapshot. 

Settings Explained
---------------------

.. _ui_settings:

.. figure:: /images/ui_settings.png
  :width: 18em
  :align: center

  The settings menu

- **Open Last Capture** 

    Playblast Plus keeps a record of the last preview generated. 
    To open this review at any point, choose this menu item. 
    Playblast Plus will open the file in the default software for the extension you are opening.

    Each host stores local settings information (like UI state) in a file called `pbp_settings.json`. It does this per host, so it's only specific to the artist. 
    It also allows the user to specify a custom executable to open the previews. To do this, locate the settings file in your default Maya/3dsMax user directory and enter the path to the executable.


- **Explore Playblast Folder** 

    Opens the local playblast folder.

- **Use Workspace** 

    If a workspace/project is set, it will use this instead of the local host directory to store the previews.

- **Template Overrides** 

    Enables the overrides. The UI will become enabled when this is toggled on. If an override option is toggled to but the main overrides are off, nothing will be implemented. 

- **Add Burnin** 

    Adds the scene name and a frame counter to the preview in the bottom right corner.

- **Copy To Clipboard** 

    Copies the encoded MP4 to the clipboard automatically, ready to paste somewhere else. 

- **Keep Intermediate Images**

    The default behaviour is for the playblast images to be deleted after the MP4 is created. Toggling this on keeps them.

- **Empty Playblast Folder** 

    Clears all previews and images from the current playblast folder.

Template Overrides
--------------------

Template overrides allow the preview to side-step some settings that may be hardcoded into the preset. If anything more complex needs to be overridden, this would be best handled in a template override.

.. _template_overrides:

.. figure:: /images/template_overrides.png
  :width: 18em
  :align: center

  The template override options

- **Show Image Plane** 

    The state of this checkbox decides if the background images/planes are displayed in the preview

- **Show Wireframe** 

    Enables the geometry wireframe (useful for model/asset turnarounds)

    The wireframe colour is set globally in the `config.json` in the `overrides>wireframe_color` key

- **Only show pbp_isolate set**

    In the Maya host, there will be a set created called `pbp_isolate`. With this option enabled, any objects placed in this set will be visible in the preview, any others will be hidden. In 3dsmax this will be implemented in a future release via a selection set of the same name.

- **Half Res** 

    Renders half resolution to make a quicker, more compact review.
  
Tokenized Output Names
-----------------------

.. _tokens_dynamic:

.. figure:: /images/output_tokens_dynamic.png
  :width: 18em
  :align: center

  Adding Dynamic Text

.. _tokens_static:

.. figure:: /images/output_tokens_dynamic_static.png
  :width: 18em
  :align: center

  Using Static Text with tokens
