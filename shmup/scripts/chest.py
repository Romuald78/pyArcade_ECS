from ecs.core.components.script import Script


class Chest(Script):

    def __init__(self, gfx, score, finalPos, compName="ChestMgr"):
        super().__init__(compName)
        self._gfx = gfx
        self._coins = []
        self._score = score
        self._chestPos = (finalPos[0],finalPos[1]+96)

    def insertCoin(self, gfxEmitter):
        # Add gfx ref into the list
        self._coins.append(gfxEmitter)

    def updateScript(self, scriptName, deltaTime):
        # If there is at least one coin to insert, open the chest
        if len(self._coins) > 0:
            # Wait for the chest to be fully closed before reopen
            if self._gfx.getCurrentAnimation() == "close" and self._gfx.isFinished():
                self._gfx.selectAnimation("open", True)
        # On the opposite, if there is no more coin, close the chest
        else:
            if self._gfx.getCurrentAnimation() == "open" and self._gfx.isFinished():
                self._gfx.selectAnimation("close", True)

        # Process all coins
        for i in range(len(self._coins)):
            k1 = 0.1
            k2 = 1-k1
            if self._coins[i].getGfx() != None:
                pos = self._coins[i].getPosition()
                newPos = (self._chestPos[0]*k1 + pos[0]*k2, self._chestPos[1]*k1 + pos[1]*k2)
                self._coins[i].setPosition(newPos)

        # remove all coins
        if len(self._coins) > 0:
            if self._coins[0].getGfx() != None:
                pos = self._coins[0].getPosition()
                if abs(pos[0]-self._chestPos[0]) < 24 and abs(pos[1]-self._chestPos[1]) < 24:
                    self._coins = self._coins[1:]
                    self._score.modify(1)
            else:
                self._coins = self._coins[1:]
                self._score.modify(1)

