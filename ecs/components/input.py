# FEATURE : improve the data structure to handle inputs
# For the moment, one instance handles one event.
# Use lists/dicts in order to make one component
# handle multiple events ?
# that should solve the fact that actioName parameter
# in callbacks is not used (so does the gamepadID)


## ============================================================
## IMPORTS
## ============================================================
from ecs.components.component import Component



## ============================================================
## INPUT UPPER CLASS
## ============================================================
class Input(Component):
    # Constants
    ALL_GAMEPADS_ID = -1
    # the upper class contains the action name of the input
    def __init__(self,actionName, compName=None):
        if compName == None:
            compName = "INPUT"
        #parent constructor
        super().__init__(compName)
        self.name = actionName
    def getType(self):
        raise ValueError("[ERR] Input getType() method not implemented yet !")
    def getActionName(self):
        return self.name


## ============================================================
## LOWER CLASSES
## ============================================================

# ----------------------------------------------------------
# KEYBOARD
# ----------------------------------------------------------
class Keyboard(Input):

    # Constructor
    def __init__(self, actionName, key, compName=None):
        if compName == None:
            compName = "KEYBOARD"
        # parent constructor
        super().__init__(actionName, compName)
        # store fields
        self.keyValue    = key
        self.risingEdge  = False    # from 'released' to 'pressed'
        self.fallingEdge = False    # from 'pressed' to 'released'
        self.value       = False    # current state

    # Event information
    def isPressed(self):
        return self.value
    def hasBeenPressed(self):
        res = self.risingEdge
        self.risingEdge = False
        return res
    def hasBeenReleased(self):
        res = self.fallingEdge
        self.fallingEdge = False
        return res

    # Field getters
    def getKey(self):
        return self.keyValue

    # Override parent method
    def getType(self):
        return Component.TYPE_KEYBOARD

    # Callback
    def keyboardEvent(self, action, isPressed):
        # Store current state
        self.value = isPressed
        # Store either rising or falling edge
        if isPressed:
            self.risingEdge  = True
        else:
            self.fallingEdge = True


# ----------------------------------------------------------
# GAMEPAD BUTTON
# ----------------------------------------------------------
class GamepadButton(Input):

    # Constructor
    def __init__(self, actionName, gamepadID, buttonName):
        # parent constructor
        super().__init__(actionName)
        # store fields
        self.ctrlID      = gamepadID
        self.button      = buttonName
        self.risingEdge  = False    # from 'released' to 'pressed'
        self.fallingEdge = False    # from 'pressed' to 'released'
        self.value       = False    # current state

    # Event information
    def isPressed(self):
        return self.value
    def hasBeenPressed(self):
        res = self.risingEdge
        self.risingEdge = False
        return res
    def hasBeenReleased(self):
        res = self.fallingEdge
        self.fallingEdge = False
        return res

    # Field getters
    def getGamepadID(self):
        return self.ctrlID
    def getButton(self):
        return self.button

    # Override parent method
    def getType(self):
        return Component.TYPE_GAMEPAD_BUTTON

    # Callback
    def gamepadButtonEvent(self, action, gamepadId, isPressed):
        # Store current state
        self.value = isPressed
        # Store either rising or falling edge
        if isPressed:
            self.risingEdge  = True
        else:
            self.fallingEdge = True


# ----------------------------------------------------------
# MOUSE BUTTON
# ----------------------------------------------------------
class MouseButton(Input):

    # Constructor
    def __init__(self, actionName, buttonName):
        # parent constructor
        super().__init__(actionName)
        # store fields
        self.button         = buttonName
        self.risingEdge     = False  # from 'released' to 'pressed'
        self.fallingEdge    = False  # from 'pressed' to 'released'
        self.value          = False  # current state
        self.lastPosition   = (-1,-1)
        self.lastRisingPos  = (-1,-1)
        self.lastFallingPos = (-1,-1)

    # Event information
    def isPressed(self):
        return self.value
    def hasBeenPressed(self):
        res = self.risingEdge
        self.risingEdge = False
        return res
    def hasBeenReleased(self):
        res = self.fallingEdge
        self.fallingEdge = False
        return res

    def getLastPosition(self):
        return self.lastPosition
    def getPressedPosition(self):
        return self.lastRisingPos
    def getReleasedPosition(self):
        return self.lastFallingPos

    # Field getters
    def getButton(self):
        return self.button

    # Override parent method
    def getType(self):
        return Component.TYPE_MOUSE_BUTTON

    # Callback
    def mouseButtonEvent(self, action, x, y, isPressed):
        # Store current state
        self.value        = isPressed
        self.lastPosition = (x,y)
        # Store either rising or falling edge
        if isPressed:
            self.risingEdge    = True
            self.lastRisingPos = (x,y)
        else:
            self.fallingEdge    = True
            self.lastFallingPos = (x,y)


# ----------------------------------------------------------
# MOUSE MOTION
# ----------------------------------------------------------
class MouseMotion(Input):

    # Constructor
    def __init__(self, actionName):
        # parent constructor
        super().__init__(actionName)
        # store fields
        self.lastPosition = (-1,-1)
        self.lastVector   = (0,0)

    # Event information
    def getLastPosition(self):
        return self.lastPosition
    def getLastVector(self):
        # Reset vector after reading
        res = self.lastVector
        self.lastVector = (0,0)
        return res

    # Override parent method
    def getType(self):
        return Component.TYPE_MOUSE_MOTION

    # Callback
    def mouseMotionEvent(self, action, x, y, dx, dy):
        self.lastPosition = (x,y)
        self.lastVector   = (dx,dy)


# ----------------------------------------------------------
# GAMEPAD AXIS
# ----------------------------------------------------------
class GamepadAxis(Input):

    # Constructor
    def __init__(self, actionName, gamepadID, axisName, deadZone=0.2, compName=None):
        if compName == None:
            compName = "AXIS"
        # parent constructor
        super().__init__(actionName, compName)
        # store fields
        self.ctrlID    = gamepadID
        self.axis      = axisName
        self.dead      = deadZone
        self.value     = 0
        self.minValue  = -0.5        # used to normalize the output
        self.maxValue  =  0.5        # used to normalize the output
        self.lastValue = 1.0

    # Event information
    def getValue(self):
        return self.value

    # Field getters
    def getGamepadID(self):
        return self.ctrlID
    def getAxis(self):
        return self.axis
    def getLastValue(self):
        return self.lastValue

    # Override parent method
    def getType(self):
        return Component.TYPE_GAMEPAD_AXIS

    # Callback
    def gamepadAxisEvent(self, action, gamepadId, analogValue):
        # Normalize value in order to take care of gamepads
        # that do not provide a full [-1.0,+1.0] output range
        # First, update min and max values
        if analogValue < self.minValue:
            self.minValue = analogValue
        if analogValue > self.maxValue:
            self.maxValue = analogValue
        # Then, check dead zone
        if abs(analogValue) < self.dead:
            analogValue = 0
        # Then, normalize
        if analogValue >= 0:
            analogValue /=  self.maxValue
        else:
            analogValue /= -self.minValue
        # Finally, store value
        if analogValue != 0:
            self.lastValue = analogValue
        self.value = analogValue

