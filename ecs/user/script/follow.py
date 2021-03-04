import math

from ecs.core.components.script import Script


class TransformFollowPhysic(Script):

    # CONSTRUCTOR
    def __init__(self, transform, physic, rotation=False, compName=None):
        super().__init__(compName)
        self._phy    = physic
        self._transf = transform
        self._rotate = rotation

    # update
    def updateScript(self, actionName, deltaTime):
        # Update position
        pos = self._phy.getPosition()
        self._transf.x = pos[0]
        self._transf.y = pos[1]
        # Update rotation
        if self._rotate:
            ang = self._phy.getAngle()
            self._transf.angle = ang




class GfxFollowTransform(Script):

    # CONSTRUCTOR
    def __init__(self, gfx, transform, offsetXY=(0,0), rotation=False, topDownZ=False, compName=None):
        super().__init__(compName)
        self._gfx    = gfx
        self._transf = transform
        self._rotate = rotation
        self._tdZ    = topDownZ
        self._offset = offsetXY

    # update
    def updateScript(self, actionName, deltaTime):
        # Update position
        pos = self._transf.position
        newPos = (pos[0]+self._offset[0], pos[1]+self._offset[1])
        self._gfx.setPosition(newPos)

        # Update rotation
        if self._rotate:
            ang = self._transf.angle
            self._gfx.setAngle(ang)

        # Update Z Index
        if self._tdZ:
            self._gfx.setZIndex( self._transf.z+self._transf.y )



class CameraFollowTransform(Script):

    def __init__(self, camera, transf, speed, minDist, mode, compName="camFollowTransf"):
        super().__init__(compName)
        self._camera  = camera
        self._transf  = transf
        self._speed   = speed
        self._minDist = minDist
        self._mode    = mode


    def updateScript(self, scriptName, deltaTime):
        pos = self._transf.position
        self._camera.moveTo(pos, self._speed, self._minDist, self._mode)