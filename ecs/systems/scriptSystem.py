# TODO allow to add several scripts with the same names !!! use a Dict of List !

## ============================================================
## IMPORTS
## ============================================================
from ecs.components.script import Script



## ============================================================
## SCRIPT MANAGER
## ============================================================

class ScriptSystem():

    ## -------------------------------------
    ## private methods
    ## -------------------------------------
    def __checkType(self, ref):
        if not isinstance(ref, Script):
            raise ValueError(f"[ERR] add script : bad object type. It should be ScriptInterface !\n{ref}")

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self):
        self.scripts = {}


    ## -------------------------------------
    ## Registering methods
    ## -------------------------------------
    def add(self, scriptName, scriptRef):
        # Check the script name is already in the dict
        if scriptName in self.scripts:
            raise ValueError(f"[ERR] add script : name '{scriptName}' already registered in the dict !")
        # check type
        self.__checkType(scriptRef)
        # Add script reference
        self.scripts[scriptName] = scriptRef

    def remove(self, scriptName):
        # browse dict and remove when found
        if scriptName in self.scripts:
            self.scripts.pop(scriptName)


    ## -------------------------------------
    ## Main method
    ## -------------------------------------
    def updateAllScripts(self, deltaTime):
        for s in self.scripts:
            self.scripts[s].updateScript(s, deltaTime)

