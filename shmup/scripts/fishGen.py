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


    def updateScript(self, scriptName, deltaTime):
        # increase timer
        self._duration += deltaTime

        # check if duration is ok
        if self._duration > 1:
            self._duration -= 1
            newFish = self._fishFactory.create()
            gfxFish = newFish.getComponentsByName("fishGfx")[0]
            # Add gfxComp to the gfx sprite list
            self._spriteList.addSprite(gfxFish)
            # Add entity to list
            self._entList.append(newFish)
            # Add gfxComp to the entity
            self._scene.addEntity(newFish)

