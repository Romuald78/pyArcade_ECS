from ecs.core.components.script import Script
from shmup.common.constants import SCREEN_HEIGHT


class DestroyBubble(Script):

    def __init__(self, entity, gfx, sprListGfx, entList, compName=None):
        super().__init__(compName)
        self._gfx = gfx
        self._entity = entity
        self._spriteList = sprListGfx
        self._entList = entList


    def updateScript(self, scriptName, deltaTime):
        if self._gfx.getPosition()[1] > SCREEN_HEIGHT + self._gfx.getHeight()/2:
            # Remove gfxComp from gfx sprite list
            self._spriteList.removeSprite(self._gfx)
            # Remove from list
            self._entList.remove(self._entity)
            # Destroy complete entity
            self._entity.destroy()
