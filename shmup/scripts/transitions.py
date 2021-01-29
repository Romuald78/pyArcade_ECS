from ecs.core.components.script import Script


class SwitchToScene(Script):

    def __init__(self, scene, keyStart, nextPush, nextSceneName=None, switchTime=None, compName=None):
        super().__init__(compName)
        self._scene     = scene
        self._key       = keyStart
        self._nextScene = nextSceneName
        self._nextPush  = nextPush
        self._maxTime   = switchTime
        self._counter   = 0

    def updateScript(self, actionName, deltaTime):
        if self._maxTime != None and self._nextScene != None:
            self._counter += deltaTime
            if self._counter >= self._maxTime:
                self._scene.selectNewScene(self._nextScene)

        if self._key.hasBeenPressed():
            self._scene.selectNewScene(self._nextPush)

