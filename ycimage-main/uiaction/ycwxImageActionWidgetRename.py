
import wx

import action.ycImageAction as ycImageAction
from uiaction.ycwxImageActionWidget import ImageActionWidget
from action.ycRenameAction import RenameAction
from uibase.ycTypes import RenameType, RenameReplaceType, RenameRemoveType, RenameAddType, RenameOccurrenceType, RenameOrderByType, RenameOrderPositionType
from ycLocalize import localize

#===============================================================
# Class ImageActionFrameRename
class ImageActionWidgetRename(ImageActionWidget):
    def __init__(self, parent, action : RenameAction, **kwargs):
        super().__init__(parent, action, **kwargs)
    
    def _create_sub_widgets(self):
        # Rename type
        self.rename_type_combo = self.add_labeled_enum_combobox('Rename Type', self.action.get_rename_type(), False)
        
        # Replace type
        self.replace_type_combo = self.add_labeled_enum_combobox('Replace Type', self.action.get_replace_type())
        self.replace_search_entry = self.add_labeled_entry('Search', self.action.get_search())
        self.replace_with_entry = self.add_labeled_entry('Replace With', self.action.get_replace_with())
        self.occurrence_type_combo = self.add_labeled_enum_combobox('Occurrence Type', self.action.get_occurrence_type())

        # Add type
        self.add_type_combo = self.add_labeled_enum_combobox('Add Type', self.action.get_add_type())
        self.add_text_entry = self.add_labeled_entry('Text', self.action.get_add_text())
        self.add_position_entry = self.add_labeled_entry('Add Position', self.action.get_left())
        self.add_before_text_entry = self.add_labeled_entry('Before Text', self.action.get_search())
        self.add_after_text_entry = self.add_labeled_entry('After Text', self.action.get_search())

        # Remove type
        self.remove_type_combo = self.add_labeled_enum_combobox('Remove Type', self.action.get_remove_type())
        self.remove_first_entry = self.add_labeled_entry('Remove First n Characters', self.action.get_left())
        self.remove_last_entry = self.add_labeled_entry('Remove Last n Characters', self.action.get_right())
        self.remove_from_entry = self.add_labeled_entry('From Position', self.action.get_left())
        self.remove_to_entry = self.add_labeled_entry('To Position', self.action.get_right())
        
        # Order type
        self.order_by_type_combo = self.add_labeled_enum_combobox('Order By Type', self.action.get_order_by_type())
        self.order_position_type_combo = self.add_labeled_enum_combobox('Position Type', self.action.get_order_position_type())
        self.order_padding_entry = self.add_labeled_entry('Padding', self.action.get_order_padding())
        self.order_start_index_entry = self.add_labeled_entry('Start Index', self.action.get_order_start_index())
        self.order_increment_entry = self.add_labeled_entry('Increment', self.action.get_order_increment())
        self.order_position_entry = self.add_labeled_entry('Position', self.action.get_order_position())

    def _show_sub_widgets(self):
        super()._show_sub_widgets()
        self._show_widget(self.rename_type_combo)
        
        rename_type = self.rename_type_combo.get_value()
        if rename_type == RenameType.ADD:
            self._show_widget(self.add_type_combo)
            add_type = self.add_type_combo.get_value()
            if add_type == RenameAddType.INSERT_POSITION:
                self._show_widget(self.add_position_entry)
            elif add_type == RenameAddType.INSERT_BEFORE:
                self._show_widget(self.add_before_text_entry)
            elif add_type == RenameAddType.INSERT_AFTER:
                self._show_widget(self.add_after_text_entry)
            self._show_widget(self.add_text_entry)
        elif rename_type == RenameType.REMOVE:
            self._show_widget(self.remove_type_combo)
            remove_type = self.remove_type_combo.get_value()
            if remove_type == RenameRemoveType.RIGHT_TRUNCATE:
                self._show_widget(self.remove_last_entry)
            elif remove_type == RenameRemoveType.LEFT_TRUNCATE:
                self._show_widget(self.remove_first_entry)
            else:
                self._show_widget(self.remove_from_entry)
                self._show_widget(self.remove_to_entry)
        elif rename_type == RenameType.REPLACE:
            replace_type = self.replace_type_combo.get_value()
            self._show_widget(self.replace_type_combo)
            if replace_type != RenameReplaceType.ALL:
                self._show_widget(self.replace_search_entry)
            self._show_widget(self.replace_with_entry)
            self._show_widget(self.occurrence_type_combo)
        elif rename_type == RenameType.ORDER:
            order_position_type = self.order_position_type_combo.get_value()
            self._show_widget(self.order_by_type_combo)
            self._show_widget(self.order_position_type_combo)
            self._show_widget(self.order_padding_entry)
            self._show_widget(self.order_start_index_entry)
            self._show_widget(self.order_increment_entry)
            if order_position_type == RenameOrderPositionType.INSERT:
                self._show_widget(self.order_position_entry)
 
    def _on_apply_internal(self):
        rename_type = self.rename_type_combo.get_value()
        self.action.set_rename_type(rename_type)
        if rename_type == RenameType.ADD:
            add_type = self.add_type_combo.get_value()
            self.action.set_add_type(add_type)
            self.action.set_add_text(self.add_text_entry.get_value())
            
            if add_type == RenameAddType.INSERT_POSITION:
                self.action.set_left(self.add_position_entry.get_value())
            elif add_type == RenameAddType.INSERT_BEFORE:
                self.action.set_sesarch(self.add_before_text_entry.get_value())
            elif add_type == RenameAddType.INSERT_AFTER:
                self.action.set_search(self.add_after_text_entry.get_value())
                
        elif rename_type == RenameType.REMOVE:
            remove_type = self.remove_type_combo.get_value()
            self.action.set_remove_type(remove_type)
            
            if remove_type == RenameRemoveType.LEFT_TRUNCATE:
                self.action.set_left(int(self.remove_first_entry.get_value()))
            elif remove_type == RenameRemoveType.RIGHT_TRUNCATE:
                self.action.set_right(int(self.remove_last_entry.get_value()))
            elif remove_type == RenameRemoveType.SUBSTRING_REMOVE:
                self.action.set_left(int(self.remove_from_entry.get_value()))
                self.action.set_right(int(self.remove_to_entry.get_value()))
                
        elif rename_type == RenameType.REPLACE:
            replace_type = self.replace_type_combo.get_value()
            self.action.set_replace_type(replace_type)
            
            if replace_type == RenameReplaceType.NORMAL or \
                replace_type == RenameReplaceType.REGEX:
                self.action.set_search(self.replace_search_entry.get_value())
            self.action.set_replace_with(self.replace_with_entry.get_value())

        elif rename_type == RenameType.ORDER:
            order_by_type = self.order_by_type_combo.get_value()
            self.action.set_order_by_type(order_by_type)
            order_position_type = self.order_position_type_combo.get_value()
            self.action.set_order_position_type(order_position_type)
            self.action.set_order_padding(self.order_padding_entry.get_value())
            self.action.set_order_start_index(self.order_start_index_entry.get_value())
            self.action.set_order_increment(self.order_increment_entry.get_value())
            if order_by_type != RenameOrderPositionType.INSERT:
                self.action.set_order_position(self.order_position_entry.get_value())

