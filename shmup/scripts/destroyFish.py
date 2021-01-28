from ecs.core.components.script import Script


class DestroyFish(Script):

    def __init__(self, entity, gfx, sprListGfx, compName=None):
        super().__init__(compName)
        self._gfx = gfx
        self._entity = entity
        self._spriteList = sprListGfx

    def updateScript(self, scriptName, deltaTime):
        if self._gfx.getPosition()[0] < self._gfx.getWidth()/2:
            # Remove gfxComp from gfx sprite list
            self._spriteList.removeSprite(self._gfx)
            # Destroy complete entity
            self._entity.destroy()
