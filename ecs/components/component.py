
## ============================================================
## COMPONENT INTERFACE
## ============================================================

class Component():

    # Use of numeric values instead of calling isinstance()
    # TODO : use some patterns like visitor instead of multiple "if" ??

    # Scripts
    TYPE_SCRIPT         = 0x1000
    # Inputs
    TYPE_KEYBOARD       = 0x2001
    TYPE_GAMEPAD_BUTTON = 0x2002
    TYPE_MOUSE_BUTTON   = 0x2004
    TYPE_MOUSE_MOTION   = 0x2008
    TYPE_GAMEPAD_AXIS   = 0x2010
    # Gfx
    # Constants
    SIMPLE    = 0x01
    ANIMATED  = 0x02
    UNLIMITED = 0x04
    LIMITED   = 0x08
    SINGLE    = 0x10
    LIST      = 0x20
    PARTICLES = 0x40
    TYPE_SIMPLE_SPRITE = 0x4000 | SIMPLE    | SINGLE
    TYPE_ANIM_SPRITE   = 0x4000 | ANIMATED  | SINGLE
    TYPE_SIMPLE_LIST   = 0x4000 | SIMPLE    | LIST
    TYPE_ANIM_LIST     = 0x4000 | ANIMATED  | LIST
    TYPE_EMITTER       = 0x4000 | UNLIMITED | PARTICLES
    TYPE_BURST         = 0x4000 | LIMITED   | PARTICLES

    # method to get the type of component
    # this way it is easier to dispatch it to the correct system
    def getType(self):
        raise ValueError("[ERR] Component getType() method has not been implemented yet !")

