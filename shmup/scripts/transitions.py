from ecs.core.components.script import Script


class SwitchToScene(Script):

    def __init__(self, scene, keyStart, nextSceneName):
        super().__init__("SwitchToScene")
        self._scene     = scene
        self._key       = keyStart
        self._nextScene = nextSceneName

    def updateScript(self, actionName, deltaTime):
        if self._key.hasBeenPressed():
            self._scene.selectNewScene(self._nextScene)

