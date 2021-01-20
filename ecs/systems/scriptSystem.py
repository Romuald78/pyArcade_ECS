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
        self._scrByName = {}
        self._scrByRef  = {}

    ## -------------------------------------
    ## Registering methods
    ## -------------------------------------
    def add(self, scriptRef):
        # check type
        self.__checkType(scriptRef)
        # Get script name
        scriptName = scriptRef.getName()
        # Add script into name dict
        if scriptName not in self._scrByName:
            self._scrByName[scriptName] = []
        if scriptRef in self._scrByName[scriptName]:
            raise ValueError("[ERR] scriptSystem add : component is already in the name dict !")
        self._scrByName[scriptName].append(scriptRef)
        # Add script into ref dict
        if scriptRef in self._scrByRef:
            raise ValueError("[ERR] scriptSystem add : component is already in the ref dict !")
        self._scrByRef[scriptRef] = scriptName

    def remove(self, scriptRef):
        # browse dict and remove when found
        if scriptRef in self._scrByRef:
            self._scrByRef.pop(scriptRef)


    ## -------------------------------------
    ## Main method
    ## -------------------------------------
    def updateAllScripts(self, deltaTime):
        for ref in self._scrByRef:
            if ref.isEnabled():
                ref.updateScript(ref.getName(), deltaTime)


