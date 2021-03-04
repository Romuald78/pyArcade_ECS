from ecs.core.components.script import Script
from games.rpg.constants import *


class MoveAI(Script):

    def __init__(self, gfx, phy, speed, compName="Move4Dirs"):
        super().__init__(compName)
        self._speed = speed
        self._gfx   = gfx
        self._phy   = phy
        self._phyTarget = None

    def setTarget(self, phyTarget):
        self._phyTarget = phyTarget

    def updateScript(self, scriptName, deltaTime):

        # Compute direction according to keyboard inputs
        move_horizontal = -1
        move_vertical   = -1
        moving          = False

        if self._phyTarget != None:
            # Get position from the target
            nextPos = self._phyTarget.getPosition()
            # Process move
            dx = self._phy.getPosition()[0] - nextPos[0]
            dy = self._phy.getPosition()[1] - nextPos[1]
            # move Horizontal
            if abs(dx)>abs(dy):
                moving = True
                if nextPos[0] < self._phy.getPosition()[0]:
                    move_horizontal = FACE_LEFT
                if nextPos[0] > self._phy.getPosition()[0]:
                    move_horizontal = FACE_RIGHT
            # move Vertical
            if abs(dx)<abs(dy):
                moving = True
                if nextPos[1]>self._phy.getPosition()[1]:
                    move_vertical = FACE_UP
                if nextPos[1]<self._phy.getPosition()[1]:
                    move_vertical = FACE_DOWN

        # Prepare moving steps
        dx = 0
        dy = 0
        # If the player is not moving
        if not moving:
            self._gfx.selectAnimation("idle")
        else:
            # If the character is actually moving in a known direction
            direction = 0
            if move_vertical != -1:
                direction = move_vertical
                dy = 2 * (2.5 - move_vertical)
            if move_horizontal != -1:
                direction = move_horizontal
                dx = 2 * (0.5 - move_horizontal)
            # Normalize speed vector
            if abs(dx)+abs(dy) > 1:
                dx *= 0.707107
                dy *= 0.707107
            dx *= self._speed
            dy *= self._speed
            # Select animation and facing direction
            self._gfx.selectAnimation("walk")
            self._gfx.selectState(direction)

        # Move the Physic
        ratio = 0.2
        vel   = self._phy.getVelocity()
        vel   = ( vel[0]*(1-ratio)+dx*ratio, vel[1]*(1-ratio)+dy*ratio )
        self._phy.setVelocity(vel)
        self._phy.setAngle(0)


