import os

config_map = {}
current_dir = os.path.dirname(os.path.abspath(__file__))
config_filename = os.path.join(current_dir, "ycconfig.cfg")
from ycLocalize import set_language

def load_config():
    global config_map, config_filename
    if not os.path.exists(config_filename):
        config_map["Language"]="en"
        config_map["ImageBackgroundColor"]="0,0,0"
    else:
        with open(config_filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    config_map[key] = value
    
        if not "Language" in config_map:
            config_map["Language"]="en"
        if not "ImageBackgroundColor" in config_map:
            config_map["ImageBackgroundColor"]="0,0,0"
    
    save_config()
    set_language(config_map["Language"])
    
def save_config():
    global config_map, config_filename 
    with open(config_filename, 'w', encoding='utf-8') as file:
        for key, value in config_map.items():
            if isinstance(value, str):
                file.write(key + "=" + value + "\n")
            else:
                file.write(key + "=" + str(value) + "\n")

def update_config(change_map):
    global config_map
    for key, value in change_map.items():
        config_map[key] = value
    save_config()

def get_config(key):
    return config_map[key] if key in config_map else ""

def get_config_language():
    return "en" if "Language" not in config_map else config_map["Language"]

def get_config_image_background_color():
    color_str = "0, 0, 0" if "ImageBackgroundColor" not in config_map else config_map["ImageBackgroundColor"]
    color = tuple(int(number) for number in color_str.split(','))
    return color
