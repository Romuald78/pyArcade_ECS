
## ============================================================
## INPUT INTERFACE
## ============================================================
class InputInterface():

    ## -------------------------------------
    ## Callbacks for input components
    ## -------------------------------------
    def cbLogicalEvent(self, action, isPressed):
        raise ValueError("[ERR] interface method not implemented yet !")

    def cbClickEvent(self, action, x, y, isPressed):
        raise ValueError("[ERR] interface method not implemented yet !")

    def cbMotionEvent(self, action, x, y, dx, dy):
        raise ValueError("[ERR] interface method not implemented yet !")

    def cbAnalogEvent(self, action, analogValue):
        raise ValueError("[ERR] interface method not implemented yet !")



## ============================================================
## INPUT MANAGER
## ============================================================
class InputManager():

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self):
        self.inputs = {}


    ## -------------------------------------
    ## Index methods
    ## -------------------------------------
    def __getKeyIndex(self, key):
        return "K" + str(key)

    def __getMouseButtonIndex(self, buttonName):
        return "M" + buttonName

    def __getGamepadButtonIndex(self, gamepadId, buttonName):
        return "G" + str(gamepadId) + "B" + buttonName

    def __getMouseMotionIndex(self):
        return "Mmotion"

    def __getGamepadAxisIndex(self,gamepadId, axisName):
        return "G" + str(gamepadId) + "B" + axisName

    def __fillData(self, idx, actionName, inputRef):
        # create index in the dictionnary
        if idx not in self.inputs:
            self.inputs[idx] = {}
        # create action name in the sub dictionnary
        if actionName not in self.inputs[idx]:
            self.inputs[idx][actionName] = []
        # fill the input reference list
        if inputRef not in self.inputs[idx][actionName]:
            self.inputs[idx][actionName].append(inputRef)


    ## -------------------------------------
    ## Registering methods
    ## -------------------------------------
    def registerKey(self, key, actionName, inputRef):
        idx = self.__getKeyIndex(key)
        self.__fillData(idx, actionName, inputRef)

    def registerMouseButton(self, buttonName, actionName, inputRef):
        idx = self.__getMouseButtonIndex(buttonName)
        self.__fillData(idx, actionName, inputRef)

    def registerGamepadButton(self, gamepadId, buttonName, actionName, inputRef):
        idx = self.__getGamepadButtonIndex(gamepadId, buttonName)
        self.__fillData(idx, actionName, inputRef)

    def registerMouseMotion(self,actionName, inputRef):
        idx = self.__getMouseMotionIndex()
        self.__fillData(idx, actionName, inputRef)

    def registerGamepadAxis(self,gamepadId, axisName, actionName, inputRef):
        idx = self.__getGamepadAxisIndex(gamepadId, axisName)
        self.__fillData(idx, actionName, inputRef)


    ## -------------------------------------
    ## Notification methods
    ## -------------------------------------
    def notifyKeyEvent(self, key, isPressed):
        idx = self.__getKeyIndex(key)
        if idx in self.inputs:
            for action in self.inputs[idx]:
                for inRef in self.inputs[idx][action]:
                    inRef.cbLogicalEvent(action, isPressed)

    def notifyMouseButtonEvent(self, buttonName, x, y, isPressed):
        idx = self.__getMouseButtonIndex(buttonName)
        if idx in self.inputs:
            for action in self.inputs[idx]:
                for inRef in self.inputs[idx][action]:
                    inRef.cbClickEvent(action, x, y, isPressed)

    def notifyGamepadButtonEvent(self, gamepadId, buttonName, isPressed):
        idx = self.__getGamepadButtonIndex(gamepadId, buttonName)
        if idx in self.inputs:
            for action in self.inputs[idx]:
                for inRef in self.inputs[idx][action]:
                    inRef.cbLogicalEvent(action, isPressed)

    def notifyMouseMotionEvent(self, x, y, dx, dy):
        idx = self.__getMouseMotionIndex()
        if idx in self.inputs:
            for action in self.inputs[idx]:
                for inRef in self.inputs[idx][action]:
                    inRef.cbMotionEvent(action, x, y, dx, dy)

    def notifyGamepadAxisEvent(self, gamepadId, axisName, analogValue):
        idx = self.__getGamepadAxisIndex(gamepadId, axisName)
        if idx in self.inputs:
            for action in self.inputs[idx]:
                for inRef in self.inputs[idx][action]:
                    inRef.cbAnalogEvent(action, analogValue)
