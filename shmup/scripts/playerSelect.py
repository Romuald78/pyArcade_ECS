from ecs.core.components.gfx import GfxAnimatedSprite
from ecs.core.components.script import Script
from random import randint

from ecs.core.main.entity import Entity
from shmup.common.constants import ZIDX_DIVERS, SCREEN_HEIGHT, MAX_PLAYERS, ZIDX_FG


class PlayerSelection(Script):

    COLORS = [ (  0,  0,200) ,
               (200,  0,  0) ,
               (  0,200,  0) ,
               (200,  0,200)
             ]

    # Choose first available color
    def _getFirstAvailableColor(self):
        for c in PlayerSelection.COLORS:
            found = False
            for p in self._players:
                if self._players[p]["color"] == c:
                    found = True
            if not found:
                return c
        return (255,255,255)

    def __init__(self, playerDict, startButton, backButton, sceneRef, prevSceneName, nextSceneName):
        super().__init__("playerSelect")
        self._players   = playerDict
        self._start     = startButton
        self._back      = backButton
        self._scene     = sceneRef
        self._prevScene = prevSceneName
        self._nextScene = nextSceneName
        self._hasStarted = False

    def updateScript(self, scriptName, deltaTime):
        # display divers according to dict
        if not self._hasStarted:
            refX = 1550
        else:
            refX = 2120
        refY = 880
        for p in self._players:
            divPos = self._players[p]["diverGfx"].getPosition()
            shdPos = self._players[p]["shadowGfx"].getPosition()
            k1 = 0.85
            k2 = 0.15
            divPos = ((divPos[0]*k1+refX*k2),(divPos[1]*k1+refY*k2))
            shdPos = ((shdPos[0]*k1+refX*k2),(shdPos[1]*k1+refY*k2))
            self._players[p]["diverGfx"].setPosition(divPos)
            self._players[p]["shadowGfx"].setPosition(shdPos)
            refY -= 340
        # if a gamepad has started, add a new player
        if self._start.hasBeenPressed() :
            lastID = self._start.getLastGamepadID()
            if not lastID in self._players:
                if len(self._players)<MAX_PLAYERS:
                    playerColor = self._getFirstAvailableColor()
                    params = {
                        "filePath": f"resources/images/divers/diver01.png",
                        "spriteBox": (4, 4, 150, 100),
                        "startIndex": 0,
                        "endIndex": 7,
                        "frameDuration": 1 / 24,
                        "size": (400, 267),
                        "textureName": f"diver{lastID}",
                        "position": (refX,SCREEN_HEIGHT + 300)
                    }
                    diverGfx = GfxAnimatedSprite(params, ZIDX_FG-50, "diverGfx")
                    diverGfx.setAngle(-28)
                    params = {
                        "filePath": f"resources/images/divers/diver02.png",
                        "spriteBox": (4, 4, 150, 100),
                        "startIndex": 0,
                        "endIndex": 7,
                        "frameDuration": 1 / 24,
                        "size": (400, 267),
                        "filterColor": playerColor,
                        "textureName": f"shadow{lastID}",
                        "position": (refX,SCREEN_HEIGHT+300)
                    }
                    shadowGfx = GfxAnimatedSprite(params, ZIDX_FG-50+1, "shadowGfx")
                    shadowGfx.setAngle(-28)
                    diverEntity = Entity()
                    diverEntity.addComponent(diverGfx)
                    diverEntity.addComponent(shadowGfx)
                    self._scene.addEntity(diverEntity)
                    self._players[lastID] = {"ctrlID"    : lastID,
                                             "diverEnt"  : diverEntity,
                                             "diverGfx"  : diverGfx,
                                             "shadowGfx" : shadowGfx,
                                             "color"     : playerColor
                                             }
            else:
                # prepare params
                i = 0
                params = {}
                for p in self._players:
                    i += 1
                    tmpName = f"Player {i}"
                    self._players[p]["playerNum"] = i
                    self._players[p]["name"]      = tmpName
                    params[tmpName]               = self._players[p]
                # Switch to in-game scene
                self._hasStarted = True
                self._scene.selectNewScene(self._nextScene, params)

        if self._back.hasBeenPressed():
            # if player list is empty, go back to previous scene
            if len(self._players) == 0:
                self._scene.selectNewScene(self._prevScene)
            # else remove the corresponding player
            else:
                lastID = self._back.getLastGamepadID()
                if lastID in self._players:
                    ent = self._players[lastID]["diverEnt"]
                    self._scene.removeEntity(ent)
                    del self._players[lastID]

    def getPlayerDict(self):
        return dict(self._players)

