
## ============================================================
## IMPORTS
## ============================================================
from ecs.components.component import Component



## ============================================================
## SCRIPT COMPONENT
## ============================================================

class Script(Component):

    # Constructor. Init the isActive flag
    def __init__(self):
        super().__init__()
        self.isActive = True

    # Setters / Getters to handle the isActive flag
    def enable(self):
        self.isActive = True
    def disable(self):
        self.isActive = False
    def isEnabled(self):
        return self.isActive
    def isDisabled(self):
        return not self.isActive

    # method to get current type
    def getType(self):
        return Component.TYPE_SCRIPT

    # method to override in the user components
    def updateScript(self, scriptName, deltaTime):
        raise ValueError("[ERR] updateScriptinterface method not implemented yet !")


