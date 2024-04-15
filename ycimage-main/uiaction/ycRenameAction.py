import re
import datetime
import os

from action.ycImageAction import Action
from uibase.ycTypes import ActionType, RenameType, RenameAddType, RenameRemoveType, RenameReplaceType, RenameOrderPositionType, RenameOrderByType, RenameOccurrenceType
from PIL import Image
import piexif

#===============================================================
# Class RenameAction
class RenameAction(Action):
    def __init__(self, name):
       super().__init__(name)
       self.rename_type = RenameType.ADD
       self.add_type = RenameAddType.SUFFIX
       self.remove_type = RenameRemoveType.LEFT_TRUNCATE
       self.replace_type = RenameReplaceType.NORMAL
       self.order_position_type = RenameOrderPositionType.SUFFIX
       self.order_by_type = RenameOrderByType.FILE_LIST
       self.occurrence_type = RenameOccurrenceType.FIRST

       self.left  = 0
       self.right = -1
       self.search = ''
       self.text = ''
       self.replace_with = ''
       self.file_index_map = {}
       self.order_padding = 3
       self.order_start_index = 1
       self.order_increment = 1
       self.order_position = 0
    
    def is_rename_action(self):
        return True
           
    def get_action_type(self):
        return ActionType.RENAME

    def get_rename_type(self):
        return self.rename_type

    def set_rename_type(self, type):
        self.rename_type = type

    def get_add_type(self):
        return self.add_type

    def set_add_type(self, type):
        self.add_type = type

    def get_remove_type(self):
        return self.remove_type

    def set_remove_type(self, type):
        self.remove_type = type

    def get_replace_type(self):
        return self.replace_type

    def set_replace_type(self, type):
        self.replace_type = type

    def get_order_position_type(self):
        return self.order_position_type

    def set_order_position_type(self, type):
        self.order_position_type = type

    def get_order_by_type(self):
        return self.order_by_type

    def set_order_by_type(self, type):
        self.order_by_type = type

    def get_left(self):
        return self.left
    
    def set_left(self, left):
        self.left = left
    
    def get_right(self):
        return self.right

    def set_right(self, right):
        self.right = right

    def get_search(self):
        return self.search

    def set_search(self, search):
        self.search = search
        
    def get_replace_with(self):
        return self.replace_with

    def set_replace_with(self, replace_with):
        self.repace_with = replace_with

    def get_add_text(self):
        return self.text

    def set_add_text(self, text):
        self.text = text
        
    def get_order_padding(self):
       return self.order_padding
   
    def set_order_padding(self, padding):
       self.order_padding = padding

    def get_order_start_index(self):
       return self.order_start_index
   
    def set_order_start_index(self, start_index):
       self.order_start_index = start_index

    def get_order_increment(self):
       return self.order_increment
   
    def set_order_increment(self, increment):
       self.order_increment = increment
       
    def get_order_position(self):
       return self.order_position
   
    def set_order_position(self, position):
       self.order_position = position

    def get_occurrence_type(self):
       return self.occurrence_type
   
    def set_occurrence_type(self, occurrence_type):
       self.occurrence_type = occurrence_type

    def _parse_text(self, text, exif):
        # seq is like {seq:d} d is one digit from 0 - 9
        #    d == 0: no leading 0 before the number
        #    d == 3: if number is less than 3 digits, 0 is added at the beginning, if more than 3 digit, output is as it is
        # {seq:0}:  number is output as 1, 2, ..., 10, ...
        # {seq:3} : number is output as 001, 002, ..., 010, ...
        # only parse the first one which start with '{seq:' and end with '}'
        # Future enhancement: parse date, time, ...
        pattern = r'\{seq:(\d)\}'
        match = re.search(pattern, text)
        if match:
            num = match.group(1)
            format_seq = f'{self.seq}' if num == 0 else ('{:0' + str(num) + '}').format(self.seq)
            text = text[:match.start()] + format_seq + text[match.end():]
            self.seq += 1
            
        pattern = r'\{etime:(.*)\}'
        match = re.search(pattern, text)
        if match:
            time_format = match.group(1)
            date = datetime.now()
            if exif:
                date_string = exif['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
                date = datetime.strptime(date_string, '%Y:%m:%d %H:%M:%S')
            format_time = date.strftime(time_format)
            text = text[:match.start()] + format_time + text[match.end():]
        
        pattern = r'\{time:(.*)\}'
        match = re.search(pattern, text)
        if match:
            time_format = match.group(1)
            date = datetime.now()
            format_time = date.strftime(time_format)
            text = text[:match.start()] + format_time + text[match.end():]
                
        return text

    # Get exif creation time, if there is no exif
    def get_exif_creation_time(self, image_path):
        found = False
        creation_time = datetime.now()
        if os.path.exists(image_path):
            creation_time = os.path.getctime(image_path)

        try:
            img = Image.open(image_path)
            exif_data = img._getexif()
            # Tag 36867 corresponds to DateTimeOriginal
            if exif_data:
                creation_time = exif_data[36867]
        except Exception as e:
            pass
        
        return creation_time

    # do preprocess for order type.
    def pre_process(self, files):
        if self.rename_type != RenameType.ORDER:
            return
        self.file_index_map = {}
        sorted_files = []
        if self.order_by_type == RenameOrderByType.FILE_LIST:
            sorted_files = files
        elif self.order_by_type == RenameOrderByType.FILE_NAME:
            sorted_files = sorted(files)
        elif self.order_by_type == RenameOrderByType.FILE_CREATION_TIME:
            sorted_files = sorted(files, key=os.path.getctime)    
        elif self.order_by_type == RenameOrderByType.FILE_EXIF_TIME:
            sorted_files = sorted(files, key=self.get_exif_creation_time)
        elif self.order_by_type == RenameOrderByType.FILE_SIZE:
            sorted_files = sorted(files, key=os.path.getsize)

        for index, filename in enumerate(sorted_files):
            self.file_index_map[filename] = index

    def post_process(self):
        # clear 
        self.file_index_map = {}
                    
    # Return new name without extension
    def get_new_base_name(self, original_file_name, file_name, exif = None):
        base_name = os.path.basename(file_name)
        split_names = os.path.splitext(base_name)
        file_name_without_ext = split_names[0]
        ext = split_names[1] if len(split_names) > 1 else ''
        
        new_name = base_name
        if self.rename_type == RenameType.REPLACE:
            parsed_text = self._parse_text(self.replace_with, exif)
            if self.replace_type == RenameReplaceType.NORMAL:
                new_name = base_name.replace(self.search, parsed_text)
            elif self.replace_type == RenameReplaceType.REGEX:
                new_name = re.sub(self.search, parsed_text, base_name, count = 1)
            elif self.replace_type == RenameReplaceType.ALL:
                new_name = parsed_text
        elif self.rename_type == RenameType.ADD:
            parsed_text = self._parse_text(self.text, exif)
            if self.add_type == RenameAddType.PREFIX:
                new_name = parsed_text + base_name
            elif self.add_type == RenameAddType.SUFFIX:
                new_name = base_name + parsed_text
            elif self.add_type == RenameAddType.INSERT_POSITION:
                if self.left >= len(base_name):
                    new_name = base_name + parsed_text
                else:
                    new_name = base_name[:self.left] + parsed_text + base_name[self.left:]
            elif self.add_type == RenameAddType.INSERT_BEFORE:
                pos = base_name.find(self.search)
                if pos == -1:
                    new_name = base_name + parsed_text
                else:
                    new_name = base_name[:pos] + parsed_text + base_name[pos:]
            elif self.add_type == RenameAddType.INSERT_AFTER:
                pos = base_name.find(self.search)
                if pos == -1:
                    new_name = base_name + parsed_text
                else:
                    pos = pos + len(self.search)
                    new_name = base_name[:pos] + parsed_text + base_name[pos:]
        elif self.rename_type == RenameType.REMOVE:
            if self.remove_type == RenameRemoveType.LEFT_TRUNCATE:
                if len > self.left:
                    new_name = base_name[self.left:]
            elif self.remove_type == RenameRemoveType.RIGHT_TRUNCATE:
                if len > self.right:
                    new_name = base_name[:-self.left]
            elif self.remove_type == RenameRemoveType.SUBSTRING_REMOVE:
                if self.right == -1 or self.right > len:
                    self.right = len
                if self.left < 0:
                    self.left = 0
                if self.left < self.right:
                    if len > self.left:
                        if self.right < len :
                            new_name = base_name[:self.left] + base_name[self.right:] 
                        else:
                            new_name = base_name[:self.left]
        elif self.rename_type == RenameType.ORDER:
            if original_file_name not in self.file_index_map:
                return file_name
            
            index = self.file_index_map[file_name]
            text =  ("%0" + str(index)) % index
            
            if self.order_position_type == RenameOrderPositionType.PREFIX:
                new_name = text + file_name
            elif self.remove_type == RenameOrderPositionType.SUFFIX:
                new_name = file_name + text
            elif self.remove_type == RenameOrderPositionType.INSERT:
                pos = min(max(0, self.order_position), len(file_name)-1)
                new_name = file_name[:pos] + text + file_name[pos:]
        
        return new_name
    
    def write_to_dict(self, dict):
        Action.write_to_dict(self, dict)
        dict['RenameType'] = self.get_enum_export_name(self.rename_type)
        if self.rename_type == RenameType.REPLACE:
            dict['ReplaceType'] =  self.get_enum_export_name(self.replace_type)
            if self.replace_type != RenameReplaceType.ALL: 
                dict['Search'] = self.search
            dict['ReplaceWith'] = self.replace_with
            dict['OccurerenceType'] =  self.get_enum_export_name(self.occurrence_type)
        elif self.rename_type == RenameType.ADD:
            dict['AddType'] = self.get_enum_export_name(self.add_type)
            dict['Text'] = self.text
            if self.add_type == RenameAddType.INSERT_POSITION:
                dict['Position'] = self.left
            elif self.add_type == RenameAddType.INSERT_BEFORE:
                dict['BeforeText'] = self.search
            elif self.add_type == RenameAddType.INSERT_AFTER:
                dict['AfterText'] = self.search
        elif self.rename_type == RenameType.REMOVE:
            dict['RemoveType'] =  self.get_enum_export_name(self.remove_type)
            if self.remove_type != RenameRemoveType.RIGHT_TRUNCATE:
                dict['Left'] = self.left
            if self.remove_type == RenameRemoveType.LEFT_TRUNCATE:
                dict['Right'] = self.right
        elif self.rename_type == RenameType.ORDER:
            dict['OrderByType'] =  self.get_enum_export_name(self.order_by_type)
            dict['OrderPositionType'] = self.get_enum_export_name(self.order_position_type)
            dict['OrderPadding'] = self.order_padding
            dict['OrderStartIndex'] = self.order_start_index
            dict['OrderIncrement'] = self.order_increment
            if self.order_position_type == RenameOrderPositionType.INSERT:
                dict['OrderPosition'] = self.order_position
                

    def read_from_dict(self, dict):
        Action.read_from_dict(self, dict)
        self.rename_type =  self.get_enum_from_export_name(RenameType, dict['RenameType'])
        if self.rename_type == RenameType.REPLACE:
            self.replace_type =  self.get_enum_from_export_name(RenameReplaceType, dict['ReplaceType'])
            if self.replace_type != RenameReplaceType.ALL: 
                self.search = dict['Search']
            self.replace_with = dict['ReplaceWith']
            self.occurrence_type = self.get_enum_from_export_name(RenameReplaceType, dict['OccurerenceType'])
        elif self.rename_type == RenameType.ADD:
            self.add_type =  self.get_enum_from_export_name(RenameAddType, dict['AddType'])
            self.text = dict['Text']
            if self.add_type == RenameAddType.INSERT_POSITION:
                self.left = dict['Position']
            elif self.add_type == RenameAddType.INSERT_BEFORE:
                self.search = dict['BeforeTxet']
            elif self.add_type == RenameAddType.INSERT_AFTER:
                self.search = dict['AfterText']
        elif self.rename_type == RenameType.REMOVE:
            self.remove_type =  self.get_enum_from_export_name(RenameRemoveType, dict['RemoveType'])
            if self.remove_type != RenameRemoveType.RIGHT_TRUNCATE:
                self.left = dict['Left']
            if self.remove_type != RenameRemoveType.LEFT_TRUNCATE:
                self.right = dict['Right']
        elif self.rename_type == RenameType.ORDER:
            self.order_by_type = self.get_enum_from_export_name(RenameOrderByType, dict['OrderByType'])
            self.order_position_type = self.get_enum_from_export_name(RenameOrderByType, dict['OrderPositionType'])
            self.order_padding = dict['OrderPadding']
            self.order_start_index = dict['OrderStartIndex']
            self.order_increment = dict['OrderIncrement']
            if self.order_position_type == RenameOrderPositionType.INSERT:
                self.order_position = dict['OrderPosition']
