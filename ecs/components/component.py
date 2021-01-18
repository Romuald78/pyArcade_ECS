
## ============================================================
## COMPONENT INTERFACE
## ============================================================
class Component():

    # Scripts
    TYPE_SCRIPT         = 1
    # Inputs
    TYPE_KEYBOARD       = 2
    TYPE_GAMEPAD_BUTTON = 3
    TYPE_MOUSE_BUTTON   = 4
    TYPE_MOUSE_MOTION   = 5
    TYPE_GAMEPAD_AXIS   = 6
    # Gfx
    TYPE_RENDER         = 7

    # method to get the type of component
    # this way it is easier to dispatch it to the correct system
    def getType(self):
        raise ValueError("[ERR] Component getType() method has not been implemented yet !")

