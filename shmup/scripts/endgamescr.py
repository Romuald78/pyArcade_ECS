from ecs.core.components.script import Script


class EndGameScr(Script):

    def __init__(self, playerEntities, compName=None):
        super().__init__(compName)
        self._ents = playerEntities
        self._ended = False

    def updateScript(self, scriptName, deltaTime):
        if not self._ended:
            for ent in self._ents:
                lf = ent.getComponentsByName("diverLife")
                if len(lf)>0:
                    if lf[0].getValue()>0:
                        return

            # Here we have reached the end of the game
            self._ended = True
            scene = self.getEntity().getScene()
            scene.selectNewScene("ENDGAME",{})
