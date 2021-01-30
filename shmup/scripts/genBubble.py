from ecs.core.components.script import Script
from shmup.factories.bubbleFactory import BubbleFactory


class GenBubble(Script):

    def __init__(self, scene, playerGfx, playerButton, sprListComp, eBubbleList, userData, compName=None):
        super().__init__(compName)
        self._gfx         = playerGfx
        self._button      = playerButton
        self._scene       = scene
        self._bubFact     = BubbleFactory(sprListComp, eBubbleList, userData)
        self._spriteList  = sprListComp
        self._eBubbleList = eBubbleList

    def updateScript(self, scriptName, deltaTime):
        # if the button has been pressed, create a new bubble entity
        # at the player gfx position, and add this entity
        if self._button.hasBeenPressed():
            gfxPos = self._gfx.getPosition()
            initPos = (gfxPos[0]+128, gfxPos[1])
            newBubble = self._bubFact.create(initPos)
            gfxBubble = newBubble.getComponentsByName("bubbleGfx")[0]
            # Add gfxComp to the gfx sprite list
            self._spriteList.addSprite(gfxBubble)
            # Add entity to the entity list
            self._eBubbleList.append(newBubble)
            # Add gfxComp to the entity
            self._scene.addEntity(newBubble)


