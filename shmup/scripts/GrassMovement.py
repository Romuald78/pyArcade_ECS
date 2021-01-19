from ecs.systems.scriptSystem import Script

class GrassMovement(Script):

    def __init__(self, characterList, grassEnt, ratio):
        # store objects
        self.charList = characterList
        self.grassList  = grassEnt.getComponent("Grass")
        self.ratio = ratio

    def updateScript(self, scriptName, deltaTime):
        DIST      = 96
        MAX_ANG   = 90
        # check if the character is near the grass sprites
        for charac in self.charList:
            charSprite = charac.getComponent("idleR").getGfx()
            for i in range(self.grassList.size()):
                # get refs
                g = self.grassList.getSprite(i)
                refChar  = charSprite.center_y - (charSprite.height/2)
                refGrass = g.center_y
                # get deltas
                dX = g.center_x - charSprite.center_x
                dY = abs(refChar-refGrass)
                # Grass is near
                if dY <= g.height//0.1 and abs(dX)<=DIST:
                    # Compute bend force according to distance
                    bendForce = ((DIST-abs(dX))/DIST)
                    finalAng = MAX_ANG*bendForce
                    # Bend according to bend force and direction
                    dir = 1
                    if dX<0:
                        dir = -1
                    # modify direction according to current grass angle
                    if abs(g.angle) > MAX_ANG * 0.5:
                        dir = -g.angle/abs(g.angle)
                    # update target angle
                    g.angle = min(finalAng, max(-finalAng, g.angle-dir*MAX_ANG/8))
                else:
                    g.angle *= self.ratio

