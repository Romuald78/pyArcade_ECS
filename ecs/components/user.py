
## ============================================================
## IMPORTS
## ============================================================
from ecs.components.component import Component



## ============================================================
## SCRIPT COMPONENT
## ============================================================

class User(Component):

    # constructor
    def __init__(self, compName=None):
        if compName == None :
            compName = "USER"
        super().__init__(compName)

    # method to get current type
    def getType(self):
        return Component.TYPE_USER

