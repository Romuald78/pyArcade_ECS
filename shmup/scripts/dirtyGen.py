from random import randint

from ecs.core.components.script import Script
from shmup.factories.dirtyFactory import DirtyFactory
from shmup.factories.fishFactory import FishFactory, SCREEN_WIDTH, SCREEN_HEIGHT


class DirtyGen(Script):


    def __init__(self, scene, entList, compName=None, decrease=True):
        super().__init__(compName)

        self._scene       = scene
        self._dirtyFactory = DirtyFactory()
        self._duration    = 0
        self._entList = entList
        self._interval = 10
        self._decr = decrease

    def updateScript(self, scriptName, deltaTime):
        # increase timer
        self._duration += deltaTime

        # check if duration is ok
        if self._duration > self._interval:
            self._interval = randint(7*100,15*100)/100
            self._duration = 0
            type = randint(0,len(DirtyFactory.DIRTS)-1)
            position = (SCREEN_WIDTH,SCREEN_HEIGHT+128)
            newDirty = self._dirtyFactory.create(type,position,self._entList)
            # Add entity to list
            self._entList.append(newDirty)
            # Add gfxComp to the entity
            self._scene.addEntity(newDirty)

