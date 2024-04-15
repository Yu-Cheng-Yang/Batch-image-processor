import os

bulk_image_lang = "en"
lang_map = {}

def get_language():
    global bulk_image_lang
    return bulk_image_lang

def read_lang_map(filename):
    local_lang_map = {}
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang")
    filename = os.path.join(dir, filename)
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                local_lang_map[key] = value
    return local_lang_map

def localize(string):
    global bulk_image_lang, lang_map
    if bulk_image_lang == "en":
        return string
    
    return lang_map.get(string, string)

def set_language(lang):
    global bulk_image_lang, lang_map
    if lang == bulk_image_lang:
        return

    bulk_image_lang = lang
    lang_map.clear()
    
    if bulk_image_lang == "fr":
        lang_map.update(read_lang_map("french.txt"))
    elif bulk_image_lang == "zh-cn":
        lang_map.update(read_lang_map("zh-cn.txt"))

        
                