import action.ycImageAction as ycImageAction

from uiaction.ycwxImageActionWidgetCrop import ImageActionWidgetCrop
from uiaction.ycwxImageActionWidgetEnhance import ImageActionWidgetEnhance
from uiaction.ycwxImageActionWidgetFilter import ImageActionWidgetFilter
from uiaction.ycwxImageActionWidgetRename import ImageActionWidgetRename
from uiaction.ycwxImageActionWidgetResize import ImageActionWidgetResize
from uiaction.ycwxImageActionWidgetRotate import ImageActionWidgetRotate
from uiaction.ycwxImageActionWidgetTransform import ImageActionWidgetTransform
from uiaction.ycwxImageActionWidgetWatermark import ImageActionWidgetWatermark
from uiaction.ycwxImageActionWidget import ImageActionWidget

def create_action_widget(parent, action: ycImageAction, **kwargs):
    action_frame = None
    if action:
        action_type = action.get_action_type()
        if action_type == ycImageAction.ActionType.RENAME:
            action_frame = ImageActionWidgetRename(parent, action, **kwargs)
        elif action_type == ycImageAction.ActionType.ROTATE:
            action_frame = ImageActionWidgetRotate(parent, action, **kwargs)
        elif action_type == ycImageAction.ActionType.RESIZE:
            action_frame = ImageActionWidgetResize(parent, action, **kwargs)
        elif action_type == ycImageAction.ActionType.WATERMARK:
            action_frame = ImageActionWidgetWatermark(parent, action, **kwargs)
        elif action_type == ycImageAction.ActionType.CROP:
            action_frame = ImageActionWidgetCrop(parent, action, **kwargs)
        elif action_type == ycImageAction.ActionType.TRANSFORM:
            action_frame = ImageActionWidgetTransform(parent, action, **kwargs)
        elif action_type == ycImageAction.ActionType.ENHANCE:
            action_frame = ImageActionWidgetEnhance(parent, action, **kwargs)
        elif action_type == ycImageAction.ActionType.FILTER:
            action_frame = ImageActionWidgetFilter(parent, action, **kwargs)
    
    return action_frame if action_frame else ImageActionWidget(parent, None, **kwargs)
