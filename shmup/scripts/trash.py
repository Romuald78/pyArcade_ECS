from ecs.core.components.script import Script


class Trash(Script):

    def __init__(self, gfx, score, finalPos, compName="TrashMgr"):
        super().__init__(compName)
        self._gfx = gfx
        self._dirty = []
        self._score = score
        self._trashPos = (finalPos[0]-64,finalPos[1]+48)

    def insertTrash(self, gfxEmitter):
        # Add gfx ref into the list
        self._dirty.append(gfxEmitter)

    def updateScript(self, scriptName, deltaTime):
        # If there is at least one coin to insert, open the chest
        if len(self._dirty) > 0:
            # Wait for the chest to be fully closed before reopen
            if self._gfx.getCurrentAnimation() == "close" and self._gfx.isFinished():
                self._gfx.selectAnimation("open", True)
        # On the opposite, if there is no more coin, close the chest
        else:
            if self._gfx.getCurrentAnimation() == "open" and self._gfx.isFinished():
                self._gfx.selectAnimation("close", True)

        # Process all coins
        for i in range(len(self._dirty)):
            k1 = 0.1
            k2 = 1-k1
            if self._dirty[i].getGfx() != None:
                pos = self._dirty[i].getPosition()
                newPos = (self._trashPos[0]*k1 + pos[0]*k2, self._trashPos[1]*k1 + pos[1]*k2)
                self._dirty[i].setPosition(newPos)

        # remove all coins
        if len(self._dirty) > 0:
            if self._dirty[0].getGfx() != None:
                pos = self._dirty[0].getPosition()
                if abs(pos[0]-self._trashPos[0]) < 24 and abs(pos[1]-self._trashPos[1]) < 24:
                    self._dirty = self._dirty[1:]
                    self._score.modify(1)
            else:
                self._dirty = self._dirty[1:]
                self._score.modify(1)

