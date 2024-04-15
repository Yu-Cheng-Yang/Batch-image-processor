import action.ycImageAction as ycImageAction
from uiaction.ycwxImageActionWidget import ImageActionWidget
from action.ycImageActionFilter import ImageActionFilter
from uibase.ycTypes import ImageFilterType, ImagePredefinedFilterType, ImageStandardFilterType

#===============================================================
# Class ImageActionWidgetFilter
class ImageActionWidgetFilter(ImageActionWidget):
    def __init__(self, parent, action : ImageActionFilter, **kwargs):
        super().__init__(parent, action, **kwargs)
        self._update_layout()

    def _create_sub_widgets(self):
        super()._create_sub_widgets()

        self.filter_type_combo = self.add_labeled_enum_combobox('Filter Type', self.action.get_filter_type(), dynamic_show = False)
        self.predefined_type_combo = self.add_labeled_enum_combobox('Predefined Filter', self.action.get_predefined_type())
        self.standard_type_combo = self.add_labeled_enum_combobox('Standard Filter', self.action.get_standard_type())
        self.radius_entry = self.add_labeled_entry('Radius', self.action.get_radius())
        self.size_entry = self.add_labeled_entry('Size', self.action.get_size())
        self.rank_entry = self.add_labeled_entry('Rank', self.action.get_rank())
        self.percent_entry = self.add_labeled_entry('Percent', self.action.get_percent())
        self.threshold_entry = self.add_labeled_entry('Threshold', self.action.get_threshold())

    def _show_sub_widgets(self):
        super()._show_sub_widgets()
        self._show_widget(self.filter_type_combo)
        
        filter_type = self.filter_type_combo.get_value()
        if filter_type == ImageFilterType.PREDEFINED_FILTER:
            self._show_widget(self.predefined_type_combo)
        elif filter_type == ImageFilterType.STANDARD_FILTER:
            standard_type = self.standard_type_combo.get_value()
            self._show_widget(self.standard_type_combo)
            if standard_type == ImageStandardFilterType.BOX_BLUR:
               self._show_widget(self.radius_entry)
            elif standard_type == ImageStandardFilterType.GAUSSIAN_BLUR:
               self._show_widget(self.radius_entry)
            elif standard_type == ImageStandardFilterType.MAX_FILTER:
               self._show_widget(self.size_entry)
            elif standard_type == ImageStandardFilterType.MEDIAN_FILTER:
               self._show_widget(self.size_entry)
            elif standard_type == ImageStandardFilterType.MIN_FILTER:
               self._show_widget(self.size_entry)
            elif standard_type == ImageStandardFilterType.MODE_FILTER:
               self._show_widget(self.size_entry)
            elif standard_type == ImageStandardFilterType.RANK_FILTER:
               self._show_widget(self.size_entry)
               self._show_widget(self.rank_entry)
            elif standard_type == ImageStandardFilterType.UNSHARP_MASK:
               self._show_widget(self.radius_entry)
               self._show_widget(self.percent_entry)
               self._show_widget(self.threshold_entry)
            
    def _on_apply_internal(self):
        filter_type = self.filter_type_combo.get_value()
        self.action.set_filter_type(filter_type)
        if filter_type == ImageFilterType.STANDARD_FILTER:
            standard_type = self.standard_type_combo.get_value()
            self.action.set_standard_type(standard_type)
            if standard_type == ImageStandardFilterType.BOX_BLUR:
                self.action.set_radius(self.radius_entry.get_value())
            elif standard_type == ImageStandardFilterType.GAUSSIAN_BLUR:
                self.action.set_radius(self.radius_entry.get_value())
            elif standard_type == ImageStandardFilterType.MAX_FILTER:
                self.action.set_size(self.size_entry.get_value())
            elif standard_type == ImageStandardFilterType.MEDIAN_FILTER:
                self.action.set_size(self.size_entry.get_value())
            elif standard_type == ImageStandardFilterType.MIN_FILTER:
                self.action.set_size(self.size_entry.get_value())
            elif standard_type == ImageStandardFilterType.MODE_FILTER:
                self.action.set_size(self.size_entry.get_value())
            elif standard_type == ImageStandardFilterType.RANK_FILTER:
                self.action.set_size(self.size_entry.get_value())
                self.action.set_rank(self.rank_entry.get_value())
            elif standard_type == ImageStandardFilterType.UNSHARP_MASK:
                self.action.set_radius(self.radius_entry.get_value())
                self.action.set_percent(self.percent_entry.get_value())
                self.action.set_threshold(self.threshold_entry.get_value())
