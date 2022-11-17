import json
from pathlib import Path

import content_management

def load_json(filepath : str) -> dict: 
    with open(filepath) as f:
        json_dict = json.load(f)
        return json_dict

def load_json_templates(template_paths : list[str]) -> list[dict]:
    json_templates = []
    for location in template_paths:
        if location:
            search_path = Path (location) / "*.json"

            for json_file in Path.glob(search_path):               
                template = load_json(json_file)
                json_templates.append(template)
    return json_templates

def get_template_locations(studio_path) -> list[str]:
    template_paths = [studio_path]
    # check if there are any project templates
    if content_management.open_pype_enabled():
        # if op is enabled but the folder doesn't exist, it will be created
        op_template_dir = content_management.get_open_pype_template_location()
        if op_template_dir:
            template_paths.append(op_template_dir)
    return template_paths



