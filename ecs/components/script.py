
## ============================================================
## IMPORTS
## ============================================================
from ecs.components.component import Component



## ============================================================
## SCRIPT COMPONENT
## ============================================================

class Script(Component):

    # method to get current type
    def getType(self):
        return Component.TYPE_SCRIPT

    # method to override in the user components
    def updateScript(self, deltaTime):
        raise ValueError("[ERR] updateScriptinterface method not implemented yet !")


