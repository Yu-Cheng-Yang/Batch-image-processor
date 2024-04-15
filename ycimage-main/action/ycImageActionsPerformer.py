from enum import Enum
import json
import os

import piexif
from PIL import Image

import action.ycImageAction as ycImageAction
from action.ycCreateAction import create_action
from action.ycRenameAction import RenameAction
from uibase.ycTypes import RenameType

class ImageFormatType(Enum):
    NONE = 0
    BMP  = 1
    JPG  = 2
    PNG  = 3
    TIFF = 4
    GIF  = 5

        
class ImageActionsPerformer():
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.files = []
        self.actions = []
        self.project_name = "Untitled.bip"
        
        self.output_folder = ""
        self.output_format = ImageFormatType.NONE
        self.output_quality = 95
        self.preserve_exif = True
        self.image_background_color = (0, 0, 0)
        
        # rename_duplicated_action is used for resolving file name conflict
        self.rename_dup_index = 1
        self.rename_dup_action = RenameAction("Rename Add 1")
        self.rename_dup_action.set_rename_type(RenameType.ADD)
        self.rename_dup_action.set_right("({seq:1})")
        
        # If overwrite is True, when conflict happens, new image will overwrite the existing file.
        # If overwrite is True, when conflict happens, new image will be saved to <name>(number).<ext>
        self.overwrite = False
    
    def get_name(self):
        return self.name
    
    def set_name(self, name: str):
        self.name = name
    
    def get_project_name(self):
        return self.project_name
    
    def set_project_name(self, project_name):
        self.project_name = project_name
        
    def get_description(self):
        return self.description
    
    def set_description(self, desciption: str):
        self.description = desciption

    def get_files(self):
        return self.files
    
    def get_file(self, index):
        if index in range(len(self.files)):
            return self.files[index]
        return ""
    
    def get_actions(self):
        return self.actions
    
    def get_action(self, index):
        if index in range(len(self.actions)):
            return self.actions[index]
        return None
    
    def get_output_format(self):
        return self.output_format
    
    def get_output_quality(self):
        return self.output_quality

    def get_output_folder(self):
        return self.output_folder
    
    def get_overwrite(self):
        return self.overwrite

    def get_image_background_color(self):
        return self.image_background_color
    
    def set_image_background_color(self, color):
        self.image_background_color = color

    def get_action_by_name(self, name : str):
        return next((action for action in self.actions if action.get_name() == name), None)
        
    def add_files(self, files: list):
        for file in files:
            self.add_file(file)
    
    def add_file(self, file: str):
        if file not in self.files:
            self.files.append(file)

    def set_files(self, files):
        self.files = files
        
    def set_actions(self, actions):
        self.actions = actions

    def add_action(self, action: ycImageAction.ImageAction):
        if action:
            # Check duplicated action. Same reference is not allowed to add
            for action1 in self.actions:
                if action is action1:
                    return ""
            # Check duplicated name and rename it to make action name unique
            new_action_name = self._get_new_action_name(action.get_name())
            action.set_name(new_action_name)
            self.actions.append(action)
            return new_action_name
        return ""
        
    def remove_action_by_name(self, name):
        for action in self.actions:
            if action.get_name() == name:
                self.actions.remove(action)
                break
        
    def set_output_folder(self, folder: str):
        self.output_folder = folder
        
    def set_output_format(self, format: ImageFormatType):
        self.output_format = format
    
    def set_output_quality(self, quality: int):
        self.output_quality = quality if quality <= 100 and quality > 0 else 95

    def set_overwrite(self, overwrite: bool):
        self.overwrite = overwrite
    
    def _split_file_name(self, file_name : str):
        folder_name = os.path.dirname(file_name)
        base_name = os.path.basename(file_name)
        split_names = os.path.splitext(base_name)
        ext = split_names[1] if len(split_names) > 1 else ""
        return folder_name, split_names[0], ext

    def get_target_file_name(self, file_name: str, action_index : int = -1, exif: dict = None):
        # Preprocess action for all names:
        if action_index < 0:
            action_index = len(self.actions)

        # Get new base name
        _, new_base_name, _ = self._split_file_name(file_name)
        for index, action in enumerate(self.actions):
            if index > action_index:
                break
            if action.is_exif_action():
                exif = action.get_new_exif(exif)
            if action.is_rename_action():
                new_base_name = action.get_new_base_name(file_name, new_base_name, exif)
        
        # Extension always use lower case
        file_ext = ".jpg"
        if self.output_format == ImageFormatType.NONE:
            _, _, extension = self._split_file_name(file_name)
            extension = extension.lower()
            if extension:
                file_ext = extension
        else:
            file_ext = "." + self.output_format.name.lower()

        new_full_name = os.path.join(self.output_folder, new_base_name + file_ext)
        
        # if not self.overwrite:
        #     # If same name file exists in the target folder, rename save image to name(index).(ext)
        #     self.rename_dup_action.set_seq(1)
        #     while os.path.isfile(new_full_name):
        #         base_name = self.rename_dup_action.get_new_base_name(new_base_name, None)
        #         new_full_name = os.path.join(self.target_folder, base_name + file_ext)
        
        return new_full_name, new_base_name + file_ext
    
    # Return image which performed by action from 0 to action_index 
    def get_image_from_actions(self, image : Image, action_index : int = -1):
        if action_index < 0:
            action_index = len(self.actions)
            
        for index, action in enumerate(self.actions):
            if (index > action_index):
                break
            
            if action.is_image_action():
                image = action.get_new_image(image)
                
        return image

    def _get_new_action_name(self, name):
        new_name = name
        index = 1
        while True:
            for action in self.actions:
                if new_name == action.get_name():
                    new_name = f"{name}({index})"
                    index += 1
                    break
            else:
                # If we didn't break the loop, there are no duplicates.
                break
        return new_name

    def run(self):
        if not os.path.exists(self.target_folder):
            os.mkdir(self.target_folder)

        self.rename_dup_index = 1
        for file_name in self.files:
            print("Processing file: " + file_name)
            if not os.path.isfile(file_name):
                print("   Error: File doesn\'t exist!")
                continue

            #Load file
            image = ycImageAction.load_image(file_name)
            if not image:
                print("   Error: not a valid image file!")
                continue
            
            # Get exif dictionary
            image_exif_info = image.info["exif"] if "exif" in image.info else None
            exif = piexif.load(image_exif_info) if image_exif_info else None
            
            # Process all image actions
            target_image = self.get_image_from_actions(image)
            target_exif = exif #self.get_exif_from_actions(exif)

            # Process all rename actions to get the new file name
            target_file_name, _ = self.get_target_file_name(file_name, -1, exif)
                
            ycImageAction.save_image(target_image, target_file_name, exif_dict = target_exif)

    def process_file(self, file):
        if not os.path.isfile(file):
            print("   Error: File doesn\'t exist!")
            return False

        #Load file
        image = ycImageAction.load_image(file)
        if not image:
            print("   Error: not a valid image file!")
            return False
        
        # Get exif dictionary
        image_exif_info = image.info["exif"] if "exif" in image.info else None
        exif = piexif.load(image_exif_info) if image_exif_info else None
        
        # Process all image actions
        target_image = self.get_image_from_actions(image)
        target_exif = exif  #self._get_exif_from_actions(exif)

        # Process all rename actions to get the new file name
        target_file_name, _ = self.get_target_file_name(file, -1, exif)
        target_file_name = self.output_folder + '\\' + target_file_name
            
        ycImageAction.save_image(target_image, target_file_name, exif_dict = target_exif)
        
        return True
        
    def save_as_json(self, file_name: str):
        dict = {}
        dict["Name"] = self.name
        dict["Description"] = self.description
        dict["OutputFolder"] = self.output_folder
        dict["OutputFormat"] = self.output_format.name.capitalize()
        dict["OutputQuality"] = self.output_quality
        dict["Overwrite"] = self.overwrite
        dict["ImageBackgroundColor"] = self.image_background_color

        dict["Files"] = self.files
        
        action_list = []
        for action in self.actions:
            dict_action = {}
            action.write_to_dict(dict_action)
            action_list.append(dict_action)
        
        dict["Actions"] = action_list

        folder = os.path.dirname(file_name)
        if not os.path.exists(folder):
            os.makedir(folder)
        json_data = json.dumps(dict)

        text_file = open(file_name, "w")
        text_file.write(json_data)
        text_file.close()

    def load_from_json(self, file_name: str):
        if not os.path.exists(file_name):
            print("Project file " + file_name + " doesn\'t exist")
            return False
        
        self.files.clear()
        self.actions.clear()
        
        xml_file = open(file_name,"r")
        json_data= xml_file.read()
        xml_file.close()
        dict = json.loads(json_data)

        self.name = dict["Name"]
        self.description = dict["Description"]
        self.target_folder = dict["OutputFolder"]
        self.output_format = ycImageAction.get_enum_from_export_name(ImageFormatType, dict["OutputFormat"])
        self.output_quality = dict["OutputQuality"]
        self.overwrite = dict["Overwrite"]
        self.image_background_color = dict["ImageBackgroundColor"]
        
        self.files = dict["Files"]

        action_dict_list = dict["Actions"]
        for action_dict in action_dict_list:
            action_type = ycImageAction.get_enum_from_export_name(ycImageAction.ActionType, action_dict["ActionName"])
            action = create_action(action_type, action_dict["Name"])
            if action:
                action.read_from_dict(action_dict)
                self.add_action(action)


        

