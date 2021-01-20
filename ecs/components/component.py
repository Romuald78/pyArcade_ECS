
## ============================================================
## COMPONENT INTERFACE
## ============================================================

class Component():

    #---------------------------------------------
    # TYPE VALUES
    #---------------------------------------------
    # Use of numeric values instead of calling isinstance()
    # TODO : use some patterns like visitor instead of multiple "if" ??

    # Scripts
    TYPE_SCRIPT_MASK    = 0x1000
    TYPE_SCRIPT         = TYPE_SCRIPT_MASK | 0x01
    # Inputs
    TYPE_INPUT_MASK     = 0x2000
    TYPE_KEYBOARD       = TYPE_INPUT_MASK | 0x01
    TYPE_GAMEPAD_BUTTON = TYPE_INPUT_MASK | 0x02
    TYPE_MOUSE_BUTTON   = TYPE_INPUT_MASK | 0x04
    TYPE_MOUSE_MOTION   = TYPE_INPUT_MASK | 0x08
    TYPE_GAMEPAD_AXIS   = TYPE_INPUT_MASK | 0x10
    # Gfx
    SIMPLE    = 0x01
    ANIMATED  = 0x02
    UNLIMITED = 0x04
    LIMITED   = 0x08
    SINGLE    = 0x10
    LIST      = 0x20
    PARTICLES = 0x40
    TYPE_GFX_MASK      = 0x4000
    TYPE_SIMPLE_SPRITE = TYPE_GFX_MASK | SIMPLE    | SINGLE
    TYPE_ANIM_SPRITE   = TYPE_GFX_MASK | ANIMATED  | SINGLE
    TYPE_SIMPLE_LIST   = TYPE_GFX_MASK | SIMPLE    | LIST
    TYPE_ANIM_LIST     = TYPE_GFX_MASK | ANIMATED  | LIST
    TYPE_EMITTER       = TYPE_GFX_MASK | UNLIMITED | PARTICLES
    TYPE_BURST         = TYPE_GFX_MASK | LIMITED   | PARTICLES
    # User defined
    TYPE_USER_MASK     = 0x8000
    TYPE_USER          = TYPE_USER_MASK | 0x01

    #---------------------------------------------
    # COMPONENT ID
    #---------------------------------------------
    # Static field
    _maxCompID = 0
    @staticmethod
    def getNewID():
        Component._maxCompID += 1
        return Component._maxCompID

    #---------------------------------------------
    # CONSTRUCTOR
    #---------------------------------------------
    # Constructor
    def __init__(self, compName):
        self._ID = Component.getNewID()
        if compName == None:
            compName = "COMP"
        self._name = f"c_{compName}_{self._ID}"

    #---------------------------------------------
    # GETTERS
    #---------------------------------------------
    def getName(self):
        return self._name

    def getID(self):
        return self._ID

    # method to get the type of component
    # this way it is easier to dispatch it to the correct system
    def getType(self):
        raise ValueError("[ERR] Component getType() method has not been implemented yet !")

