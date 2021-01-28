from ecs.core.components.script import Script
from shmup.factories.fishFactory import FishFactory


class FishGen(Script):


    def __init__(self, scene, sprListComp, compName=None):
        super().__init__(compName)

        self._scene       = scene
        self._fishFactory = FishFactory()
        self._duration    = -10
        self._spriteList = sprListComp


    def updateScript(self, scriptName, deltaTime):
        # increase timer
        self._duration += deltaTime

        # check if duration is ok
        if self._duration > 1:
            self._duration -= 1
            newFish = self._fishFactory.create(self._spriteList)
            gfxFish = newFish.getComponentsByName("fishGfx")[0]
            # Add gfxComp to the gfx sprite list
            self._spriteList.addSprite(gfxFish)
            # Add gfxComp to the entity
            self._scene.addEntity(newFish)

