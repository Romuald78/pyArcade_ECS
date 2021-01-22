from ecs.core.components.script import Script



class PauseToggle(Script):

    def __init__(self, scn, key, compName=None):
        super().__init__(compName)
        # store components
        self.scene = scn
        self.key   = key

    def updateScript(self, scriptName, deltaTime):
        if self.key.hasBeenPressed():
            if self.scene.isPaused():
                self.scene.resume()
            else:
                self.scene.pause()


class Pause2Buttons(Script):

    def __init__(self, scn, bPause, bResume, compName=None):
        super().__init__(compName)
        # store components
        self.scene = scn
        self.buttonP = bPause
        self.buttonR = bResume

    def updateScript(self, scriptName, deltaTime):
        if self.buttonP.hasBeenPressed():
            if not self.scene.isPaused():
                self.scene.pause()
        if self.buttonR.hasBeenPressed():
            if self.scene.isPaused():
                self.scene.resume()
