## v1.41 Changelog (2023-05-03)

> Description - Small code tweaks to incorporate new templates

### Upgrade Steps
* Overwrite the local install. (`Documents/Maya`)
* Point the `PYTHONPATH` to a new version folder

### New Features
* Shows the version in the settings menu.
* Stores and restores the last selected template. (similar to the last camera)


### Bug Fixes
* `__init__()` load order adjusted to allow templates to be imported before being set in the UI.


### Other Changes
* Added a `studio_previs_lighting` template to render lighting setups.
