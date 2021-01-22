
## ============================================================
## COMPONENT INTERFACE
## ============================================================

class Component():

    #---------------------------------------------
    # TYPE VALUES
    #---------------------------------------------
    # Use of numeric values instead of calling isinstance()
    # TASK : use some patterns like visitor instead of multiple "if" ??

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
    TYPE_IDLE_MASK     = 0x8000
    TYPE_IDLE          = TYPE_IDLE_MASK | 0x01
    # User Strings
    TYPE_INFO = {
        TYPE_SCRIPT         : {"name" : "Script",
                               "color": (255,64,64)},
        TYPE_MOUSE_BUTTON   : {"name": "MouseButton",
                               "color": (80,80,255)},
        TYPE_MOUSE_MOTION   : {"name": "MouseMotion",
                               "color": (80,80,255)},
        TYPE_KEYBOARD       : {"name": "Key",
                               "color": (128,128,255)},
        TYPE_GAMEPAD_BUTTON : {"name": "GamepadButton",
                               "color": (160,160,255)},
        TYPE_GAMEPAD_AXIS   : {"name": "GamepadAxis",
                               "color": (160,160,255)},
        TYPE_SIMPLE_SPRITE  : {"name": "FixedSprite",
                               "color": (255,255,0)},
        TYPE_ANIM_SPRITE    : {"name": "AnimSprite",
                               "color": (255,255,0)},
        TYPE_SIMPLE_LIST    : {"name": "FixedSpriteList",
                               "color": (192,192,0)},
        TYPE_ANIM_LIST      : {"name": "AnimSpriteList",
                               "color": (192,192,0)},
        TYPE_EMITTER        : {"name": "Emitter",
                               "color": (255,255,64)},
        TYPE_BURST          : {"name": "Burst",
                               "color": (255,255,64)},
        TYPE_IDLE           : {"name": "User",
                               "color": (192,192,192)},
    }


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
        # By default this component is disabled when the
        # scene is on pause; That means NO UPDATE (scripts or animated sprites)
        self.execOnPause = False
        # By default this script is enabled
        self.isActive = True


    #---------------------------------------------
    # SETTERS
    #---------------------------------------------
    # On Pause behavior
    def enableOnPause(self):
        self.execOnPause = True
    def disableOnPause(self):
        self.execOnPause = False


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
    def getTypeName(self):
        t = self.getType()
        s = Component.TYPE_INFO[t]["name"]
        return s
    def getTypeColor(self):
        t = self.getType()
        c = Component.TYPE_INFO[t]["color"]
        return c

    # On Pause behavior
    def isEnabledOnPause(self):
        return self.execOnPause
    def isDisabledOnPause(self):
        return not self.execOnPause

    def enable(self):
        self.isActive = True
    def disable(self):
        self.isActive = False
    def isEnabled(self):
        return self.isActive
    def isDisabled(self):
        return not self.isActive
