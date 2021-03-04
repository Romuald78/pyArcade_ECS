import math

from ecs.core.components.idle import Idle
from ecs.core.components.script import Script


class ZoomCamera(Script):

    # CONSTRUCTOR
    def __init__(self, camera, keyP, keyM, compName=None):
        super().__init__(compName)
        self._cam  = camera
        self._keyP = keyP
        self._keyM = keyM

    # update
    def updateScript(self, actionName, deltaTime):
        if self._keyP.isPressed():
            self._cam.zoom += 0.01
            print(self._cam.zoom)
        if self._keyM.isPressed():
            self._cam.zoom -= 0.01
            print(self._cam.zoom)


class SwitchCameras(Script):

    def __init__(self, scene, cameraList, keyP, keyM, compName=None):
        super().__init__(compName)
        self._scene   = scene
        self._camList = cameraList
        self._index   = 0
        self._keyP    = keyP
        self._keyM    = keyM

    def updateScript(self, scriptName, deltaTime):
        # Get nb cameras
        nbCams = len(self._camList)
        # If select next cam
        if self._keyP.hasBeenPressed():
            self._index = (self._index+1) % nbCams
            self._scene.setActiveCamera(self._camList[self._index])
        # If select previous cam
        if self._keyM.hasBeenPressed():
            self._index = (self._index + nbCams - 1) % nbCams
            self._scene.setActiveCamera(self._camList[self._index])
