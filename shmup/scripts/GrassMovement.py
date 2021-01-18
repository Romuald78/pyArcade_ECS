from ecs.systems.script import Script
import random
from random import randint


class GrassMovement(Script):

    def __init__(self, characterEnt, grassEnt, ratio):
        # store objects
        self.charSprite = characterEnt.getComponent("Panda").getGfx()
        self.grassList  = grassEnt.getComponent("Grass")
        self.moveComp   = characterEnt.getComponent("inputAnalogX")
        self.ratio = ratio

    def updateScript(self, scriptName, deltaTime):
        DIST    = 64
        MAX_ANG = 85
        # check if the character is near the grass sprites
        for i in range(self.grassList.size()):
            g = self.grassList.getSprite(i)
            # get refs
            refChar  = self.charSprite.center_y - (self.charSprite.height/2)
            refGrass = g.center_y
            # get deltas
            dX = g.center_x - self.charSprite.center_x
            dY = abs(refChar-refGrass)
            # Set rotation by default
            random.seed((1+g.center_x)*(2+g.center_y))
            g.angle *= self.ratio + (random.random() * ((1-self.ratio)//2) )
            if abs(g.angle) < 1 :
                g.angle = 0
            # Check dY
            if dY <= g.height//0.1:
                if abs(dX)<=DIST:
                    # Turn grass around character AND according to direction
                    if dX >= 0:

                        if self.moveComp.getLastValue() > 0:
                            g.angle = max(-(DIST - dX) * MAX_ANG / DIST, g.angle - (MAX_ANG / 2))
                    else:
                        if self.moveComp.getLastValue() < 0:
                            g.angle = min((DIST+dX) * MAX_ANG / DIST, g.angle + (MAX_ANG / 2))
