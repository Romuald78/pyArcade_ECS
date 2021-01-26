from ecs.core.components.script import Script


class PlayerSelection(Script):

    def __init__(self, playerDict, startButton, backButton, sceneRef, prevSceneName, nextSceneName):
        super().__init__("playerSelect")
        self._players   = playerDict
        self._start     = startButton
        self._back      = backButton
        self._scene     = sceneRef
        self._prevScene = prevSceneName
        self._nextScene = nextSceneName

    def updateScript(self, scriptName, deltaTime):
        # if a gamepad has started
        if self._start.hasBeenPressed():
            lastID = self._start.getLastGamepadID()
            if not lastID in self._players:
                self._players[lastID] = {"ctrlID"   : lastID,
                                         "color"    : (255,255,255),
                                         "shipType" : "fighter"
                                         }
            else:
                # prepare params
                i = 0
                params = {}
                for p in self._players:
                    i += 1
                    tmpName = f"Player {i}"
                    self._players[p]["playerNum"] = i
                    self._players[p]["name"] = tmpName
                    params[tmpName]          = self._players[p]
                # Switch to in-game scene
                self._scene.selectNewScene(self._nextScene, params)
        if self._back.hasBeenPressed():
            # if player list is empty, go back to previous scene
            if len(self._players) == 0:
                self._scene.selectNewScene(self._prevScene)
            # else remove the corresponding player
            else:
                lastID = self._back.getLastGamepadID()
                if lastID in self._players:
                    del self._players[lastID]

    def getPlayerDict(self):
        return dict(self._players)

