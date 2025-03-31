## v1.50 Changelog (2025-03-31)

> Description - Long overdue update to PySide6 

Now compatible with Maya 2025

### Upgrade Steps
* Overwrite the local install. (`Documents/Maya`)
* Point the `PYTHONPATH` to this new version folder

### Bug Fixes

* Fixed the camera token issue that plagued previous versions


Other potential fixes - 
- Could easily prune this from the dictionary manually. But I'd rather leave `capture.py` as it is and add the code to `maya_preview.pre_process`  
- remove ```"viewport_options": {"gpuCacheDisplayFilter": true}``` from the stock templates

### Other Changes
* Some UI tweaks to reflect THE LINE's branding update
* Added a refresh button to the camera list
* Upgraded the default FFPMEG version




