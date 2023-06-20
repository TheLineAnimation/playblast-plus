## v1.42 Changelog (2023-06-20)

> Description - Small code tweaks to incorporate new templates

### Upgrade Steps
* Overwrite the local install. (`Documents/Maya`)
* Point the `PYTHONPATH` to this new version folder

### Bug Fixes
* Noticed an issue with a new maya install if the `gpuCache` plugin wasn't enabled. Seems reasonable to ask to switch it on and then do this so it an work correctly. The issue was that `capture.py` wouldn't filter the `gpucachedisplayfilter` from the template if the plugin wasn't loaded. 

```python
# capture.py line 715 
plugins = cmds.pluginDisplayFilter(query=True, listFilters=True)
```
This would result in an empty list, meaning the template would error.

Other potential fixes - 
- Could easily prune this from the dictionary manually. But I'd rather leave `capture.py` as it is and add the code to `maya_preview.pre_process`  
- remove ```"viewport_options": {"gpuCacheDisplayFilter": true}``` from the stock templates

### Other Changes
* Added a `studio_rigging_joints_visible` and `studio_rigging_visible` template to render animation setups. these show control shapes only and controls shapes and joints. 




