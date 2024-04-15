
from action.ycImageActionCrop import ImageActionCrop
from action.ycImageActionEnhance import ImageActionEnhance
from action.ycImageActionFilter import ImageActionFilter
from action.ycImageActionResize import ImageActionResize
from action.ycImageActionRotate import ImageActionRotate
from action.ycImageActionTransform import ImageActionTransform
from action.ycImageActionWatermark import ImageActionWatermark

from action.ycRenameAction import RenameAction
from uibase.ycTypes import ActionType

def create_action(action_type: ActionType, name: str):
    action = None
    if action_type == ActionType.WATERMARK:
        action = ImageActionWatermark(name)
    elif action_type == ActionType.RESIZE:
        action = ImageActionResize(name)
    elif action_type == ActionType.ROTATE:
        action = ImageActionRotate(name)
    elif action_type == ActionType.CROP:
        action = ImageActionCrop(name)
    elif action_type == ActionType.TRANSFORM:
        action = ImageActionTransform(name)
    elif action_type == ActionType.ENHANCE:
        action = ImageActionEnhance(name)
    elif action_type == ActionType.FILTER:
        action = ImageActionFilter(name)
    elif action_type == ActionType.RENAME:
        action = RenameAction(name)

    return action
