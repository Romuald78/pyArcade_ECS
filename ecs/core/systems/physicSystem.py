

## ============================================================
## IMPORTS
## ============================================================
import pymunk

from ecs.core.components.physic import Physic



## ============================================================
## SCRIPT MANAGER
## ============================================================

class PhysicSystem():

    ## -------------------------------------
    ## PRIVATE METHODS
    ## -------------------------------------
    def __checkType(self, ref):
        if not isinstance(ref, Physic):
            raise ValueError(f"[ERR] add physic : bad object type. It should be Physic !\n{ref}")


    ## -------------------------------------
    ## CONSTRUCTOR
    ## -------------------------------------
    def __init__(self, gravity=(0,0), damping=0.01):
        # Create component dicts
        self._scrByName = {}
        self._scrByRef = {}
        # Create physic environment
        self._space         = pymunk.Space()
        self._space.gravity = gravity
        self._space.damping = damping
        # Get debug info
        self._info = pymunk.SpaceDebugDrawOptions()


    ## -------------------------------------
    ## (UN)REGISTERING
    ## -------------------------------------
    def add(self, phyRef):
        # check type
        self.__checkType(phyRef)
        # Get script name
        scriptName = phyRef.getName()
        # Add script into name dict
        if scriptName not in self._scrByName:
            self._scrByName[scriptName] = []
        if phyRef in self._scrByName[scriptName]:
            raise ValueError("[ERR] physicSystem add : component is already in the name dict !")
        self._scrByName[scriptName].append(phyRef)
        # Add script into ref dict
        if phyRef in self._scrByRef:
            raise ValueError("[ERR] physicSystem add : component is already in the ref dict !")
        self._scrByRef[phyRef] = scriptName
        # Add the body into the physic space
        bdyList = phyRef.getBodyList()
        self._space.add(bdyList[0][0],bdyList[0][1])

    def remove(self, phyRef):
        # Remove from ref dict
        if phyRef in self._scrByRef:
            self._scrByRef.pop(phyRef)
        # Remove from name dict
        for nam in self._scrByName:
            if phyRef in self._scrByName[nam]:
                self._scrByName[nam].remove(phyRef)
        # Remove bodies from physic space
        # TODO !!!!


    ## -------------------------------------
    ## UPDATE METHOD
    ## -------------------------------------
    def updatePhysicEngine(self, deltaTime, isOnPause):

        # TODO handle the isEnabled field for each component
        # What disable means (removing body from space ? or putting body as a sensor ?)
        # May be during the enable/disable call we can modify the data instead of during
        # the update methode right here (?)

        # TODO : how to handle the enableOnPause field for physic components ??

        # update physic world (except if we are on pause)
        if not isOnPause:
            self._space.step(deltaTime)
            # display info
            # self._space.debug_draw(self._info)


    ## -------------------------------------
    ## DRAW DEBUG INFO
    ## -------------------------------------
    def drawDebug(self):
        for phyComp in self._scrByRef:
            phyComp.drawDebug()


    ## -------------------------------------
    ## PHYSIC WORLD
    ## -------------------------------------
    def getPhysicWorld(self):
        return self._space


