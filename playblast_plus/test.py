import lib.preset as preset

from pathlib import Path

settings = preset.load_json('.\settings.json')
settings['openpype']
st = (settings['studio_templates'])
paths = preset.get_project_locations (st)
templates = preset.load_templates ( paths )

print ( f'settings {settings}')
print ( f'templates {templates}')

ffmpeg_path = Path(settings['ffmpeg']['path']).resolve()
print ( f'ffmpeg_path {ffmpeg_path}\\ffmpeg.exe')