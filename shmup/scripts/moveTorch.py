from random import randint

from ecs.core.components.script import Script
from shmup.common.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class MoveTorch(Script):

    def __init__(self, light, diagonal=False,compName="MoveTorch"):
        super().__init__(compName)
        self._light   = light
        self._counter = 0
        self._dest = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
        self._diag = diagonal

    def updateScript(self, scriptName, deltaTime):
        # increase counter
        self._counter += deltaTime
        # Set new random position
        duration = 1.5
        if self._counter >= duration:
            self._counter -= duration
            x = randint(0,2*SCREEN_WIDTH//3)+(SCREEN_WIDTH//6)
            if self._diag:
                y = randint(0, SCREEN_HEIGHT // 2)
                if x >= SCREEN_WIDTH//2:
                    y *= 2
            else:
                y = randint(0, 2*SCREEN_HEIGHT // 3)+(SCREEN_HEIGHT//6)
            position = (x,y)
            self._dest = position
        # MOve light torch according to current position and destination
        curPos = self._light.getPosition()
        k1 = 0.05
        k2 = 1-k1
        newPos = (curPos[0]*k2+self._dest[0]*k1,curPos[1]*k2+self._dest[1]*k1)
        self._light.setPosition(newPos)