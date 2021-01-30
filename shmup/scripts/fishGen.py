from ecs.core.components.script import Script
from shmup.factories.fishFactory import FishFactory


class FishGen(Script):


    def __init__(self, scene, sprListComp, entList, compName=None):
        super().__init__(compName)

        self._scene       = scene
        self._fishFactory = FishFactory(sprListComp, entList)
        self._duration    = 0
        self._spriteList = sprListComp
        self._entList = entList
        self._interval = 3


    def updateScript(self, scriptName, deltaTime):
        # increase timer
        self._duration += deltaTime

        # decrease interval
        self._interval -= 0.0001
        self._interval = max(0.25, self._interval)

        # check if duration is ok
        if self._duration > self._interval:
            self._duration -= self._interval
            newFish = self._fishFactory.create()
            gfxFish = newFish.getComponentsByName("fishGfx")[0]
            # Add gfxComp to the gfx sprite list
            self._spriteList.addSprite(gfxFish)
            # Add entity to list
            self._entList.append(newFish)
            # Add gfxComp to the entity
            self._scene.addEntity(newFish)

