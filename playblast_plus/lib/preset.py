import json
from pathlib import Path

from . import content_management
from . import settings
from .utils import Parsing

from typing import List, Dict

# def load_json(filepath : str) -> dict: 
#     with open(filepath) as f:
#         json_dict = json.load(f)
#         return json_dict

def load_templates(template_paths : List[str]) -> List[Dict]:
    json_templates = []
    print (f'template paths {template_paths}')
    for location in template_paths:
        if location:
            location = Path (location).resolve() 
            print (f'location {location}')

            for json_file in location.glob('*.json'):               
                template = Parsing.load_json_from_file(json_file)
                json_templates.append({ f"{json_file.stem}":template})
    return json_templates

def get_project_locations(studio_path : str) -> List[str]:
    template_paths = [studio_path]
    # check if there are any project templates
    if settings.open_pype_enabled() and content_management.open_pype_enabled():
        # if op is enabled but the folder doesn't exist, it will be created
        op_template_dir = content_management.get_open_pype_template_location()
        if op_template_dir:
            template_paths.append(op_template_dir)
    return template_paths



