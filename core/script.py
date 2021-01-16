
## ============================================================
## SCRIPT INTERFACE
## ============================================================
class ScriptInterface():

    ## -------------------------------------
    ## Callbacks for script components
    ## -------------------------------------
    def updateScript(self, deltaTime):
        raise ValueError("[ERR] interface method not implemented yet !")



## ============================================================
## SCRIPT MANAGER
## ============================================================
class ScriptManager():

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
            raise ValueError("[ERR] add : script already registered in the dict !")
        # Add script reference
        self.scripts[scriptName] = scriptRef

    def remove(self, ref):
        for s in self.scripts:
            if self.scripts[s] == ref:
                self.scripts.pop(s)
                return


    ## -------------------------------------
    ## Main method
    ## -------------------------------------
    def updateAllScripts(self, deltaTime):
        for s in self.scripts:
            self.scripts[s].updateScript(deltaTime)

