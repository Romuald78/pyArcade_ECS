# TODO allow to add several components with the same names !!! use a Dict of List !

## ============================================================
## IMPORTS
## ============================================================



## ============================================================
## IDLE MANAGER
## ============================================================
from ecs.components.user import User


class IdleSystem():

    ## -------------------------------------
    ## private methods
    ## -------------------------------------
    def __checkType(self, ref):
        if not isinstance(ref, User):
            raise ValueError(f"[ERR] add script : bad object type. It should be ScriptInterface !\n{ref}")

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self):
        self.idleComps = {}


    ## -------------------------------------
    ## Registering methods
    ## -------------------------------------
    def add(self, idleRef):
        # check type
        self.__checkType(idleRef)
        # get name
        idleName = idleRef.getName()
        # Check the component name is already in the dict
        if idleName in self.idleComps:
            raise ValueError(f"[ERR] add script : name '{idleName}' already registered in the dict !")
        # Add script reference
        self.idleComps[idleName] = idleRef

    def remove(self, scriptName):
        pass


