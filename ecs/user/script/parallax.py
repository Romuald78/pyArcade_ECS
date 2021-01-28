from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite
from ecs.core.components.script import Script
from shmup.common.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Parallax(Script):

    def __init__(self, entity, filePath, fileSize, screenSize, zIndex, speed, compName="Parallax"):
        # Parent
        super().__init__(compName)
        # Init fields
        self._gfxList = []
        self._speed   = speed
        self._size    = fileSize
        self._screen = screenSize
        # Create all gfx to fit the screen width
        maxi = screenSize[0]/fileSize[0]
        maxi = int(maxi+1)
        params = {
            "filePath": filePath,
            "size": fileSize,
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"parallax{self.getID()}",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        for i in range(maxi):
            # create Gfx component
            params["position"] = ((SCREEN_WIDTH*i)+(SCREEN_WIDTH//2), SCREEN_HEIGHT // 2)
            tmpGfx = GfxAnimatedSprite(params, zIndex, f"gfx{compName}{i}")
            # add it to the field
            self._gfxList.append(tmpGfx)
            # add gfx to the entity
            entity.addComponent(tmpGfx)

    def updateScript(self, scriptName, deltaTime):
        # update all sprites moving
        for gfx in self._gfxList:
            gfx.move(deltaTime*60*self._speed,0)
        # prepare local vars
        firstPos = self._gfxList[0].getPosition()
        lastPos = self._gfxList[-1].getPosition()
        width = self._size[0]
        half = width // 2
        # Check if the border picture is outside the screen
        if self._speed < 0:
            # speed negative,  so the parallax to the left
            if firstPos[0] < -half:
                # Put gfx to the full right
                self._gfxList[0].setPosition((lastPos[0]+width,lastPos[1]))
                # put it into the end of the list
                self._gfxList = self._gfxList[1:] + [self._gfxList[0],]
        else:
            # speed positive,  so the parallax to the right
            if lastPos[0] > self._screen[0]+half:
                # Put gfx to the full right
                self._gfxList[-1].setPosition((firstPos[0] - width, firstPos[1]))
                # put it into the beginning of the list
                self._gfxList = [self._gfxList[-1],] + self._gfxList[:-1]

