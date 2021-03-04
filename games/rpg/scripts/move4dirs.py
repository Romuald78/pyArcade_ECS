from ecs.core.components.script import Script
from games.rpg.constants import *


class Move4Dirs(Script):

    def __init__(self, gfx, phy, keyL, keyR, keyU, keyD, speed, compName="Move4Dirs"):
        super().__init__(compName)
        self._speed = speed
        self._gfx   = gfx
        self._phy   = phy
        self._keyL  = keyL
        self._keyR  = keyR
        self._keyU  = keyU
        self._keyD  = keyD


    def updateScript(self, scriptName, deltaTime):

        # Compute direction according to keyboard inputs
        move_horizontal = -1
        move_vertical   = -1
        moving          = False

        moveL = self._keyL.isPressed()
        moveR = self._keyR.isPressed()
        moveU = self._keyU.isPressed()
        moveD = self._keyD.isPressed()

        if moveU and not moveD:
            move_vertical = FACE_UP
            moving = True
        if not moveU and moveD:
            move_vertical = FACE_DOWN
            moving = True
        if moveL and not moveR:
            move_horizontal = FACE_LEFT
            moving = True
        if not moveL and moveR:
            move_horizontal = FACE_RIGHT
            moving = True

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
