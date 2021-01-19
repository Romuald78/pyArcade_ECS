
## ============================================================
## IMPORTS
## ============================================================
from ecs.components.component import Component
from utils import *



## ============================================================
## GFX UPPER CLASS
## ============================================================
class Gfx(Component):

    # upper class contains the zIndex field
    def __init__(self):
        self.zIndex = 0

    # Get arcade gfx object
    def getGfx(self):
        raise ValueError("[ERR] gfx : getGfx method seems to be not implemented !")
    # type method
    def getType(self):
        raise ValueError("[ERR] gfx : getType method has not been implemented yet !")

    # Z-Index
    def getZIndex(self):
        return self.zIndex
    def setZIndex(self,newZ):
        self.zIndex = newZ

    # Position
    def move(self, dx, dy):
        raise ValueError("[ERR] gfx : move method has not been implemented yet !")
    def setPosition(self, newPos):
        raise ValueError("[ERR] gfx : setPosition method has not been implemented yet !")
    def getPosition(self):
        raise ValueError("[ERR] gfx : getPosition method has not been implemented yet !")

    # Orientation
    # TODO add the way to rotate from any pivot position
    def rotate(self, offset, multiplier, pivotPos=None):
        # first multiply then add offset
        raise ValueError("[ERR] gfx : rotate method has not been implemented yet !")
    def setAngle(self, newAngle, pivotPos=None):
        raise ValueError("[ERR] gfx : setAngle method has not been implemented yet !")
    def getAngle(self):
        raise ValueError("[ERR] gfx : getAngle method has not been implemented yet !")

    # Scale
    def setScale(self,newScale):
        raise ValueError("[ERR] gfx : setScale method has not been implemented yet !")
    def getScale(self):
        raise ValueError("[ERR] gfx : getScale method has not been implemented yet !")

    # TODO add other methods to manipulate Gfx objects


## ============================================================
## GFX COMPONENTS
## ============================================================

#-----------------------------------
class GfxSimpleSprite(Gfx):

    # Constructor
    def __init__(self,params, zIdx=0):
        # call to parent constructor
        super().__init__()
        # create Gfx element
        self.gfx = createSimpleSprite(params)
        self.setZIndex(zIdx)
    # Override parent methods
    def getType(self):
        return Component.TYPE_SIMPLE_SPRITE
    def getGfx(self):
        return self.gfx

    # Position
    def move(self, dx, dy):
        self.gfx.center_x += dx
        self.gfx.center_y += dy
    def setPosition(self, newPos):
        self.gfx.center_x = newPos[0]
        self.gfx.center_y = newPos[1]
    def getPosition(self):
        return (self.gfx.center_x, self.gfx.center_y)

    # Orientation
    def rotate(self, offset, multiplier=1.0, pivotPos=None):
        # TODO ? is there a problem not to be in a specific range like [0-360] or [-180-180] ?
        self.gfx.angle *= multiplier
        self.gfx.angle += offset
    def setAngle(self, newAngle, pivotPos=None):
        self.gfx.angle = newAngle
    def getAngle(self):
        return self.gfx.angle

    # Scale
    def setScale(self,newScale):
        self.gfx.scale = newScale
    def getScale(self):
        return self.gfx.scale

#-----------------------------------
class GfxSimpleSpriteList(Gfx):

    # Constructor
    def __init__(self, zIdx=0):
        # call to parent constructor
        super().__init__()
        # create Gfx element
        self.gfx = arcade.SpriteList()
        self.setZIndex(zIdx)

    # Override parent method
    def addSprite(self, params):
        newSprite = createSimpleSprite(params)
        self.gfx.append(newSprite)
    def getType(self):
        return Component.TYPE_SIMPLE_LIST
    def getGfx(self):
        return self.gfx

    # orientation
    def rotate(self, offset, mult, pivotPos=None):
        for gfx in self.gfx:
            gfx.angle *= mult
            gfx.angle += offset

    # List management
    def size(self):
        return len(self.gfx)
    def getSprite(self,index):
        return self.gfx[index]
    # TODO add component methods





















#-----------------------------------
class GfxAnimatedSprite(Gfx):

    # Constructor
    def __init__(self,params):
        # call to parent constructor
        super().__init__()
        # create Gfx element
        self.gfx = createAnimatedSprite(params)
    # Override parent method
    def getType(self):
        return Component.TYPE_ANIM_SPRITE
    # TODO add component methods




#-----------------------------------
class GfxAnimatedSpriteList(Gfx):

    # Constructor
    def __init__(self):
        # call to parent constructor
        super().__init__()
        # create Gfx element
        self.gfx = arcade.SpriteList()
    # Override parent method
    def addSprite(self, params):
        newSprite = createAnimatedSprite(params)
        self.gfx.append(newSprite)
    def getType(self):
        return Component.TYPE_ANIM_LIST
    # TODO add component methods


#-----------------------------------
class GfxSimpleEmitter(Gfx):

    # Constructor
    def __init__(self, params):
        # call to parent constructor
        super().__init__()
        # create Gfx element
        self.gfx = createParticleEmitter(params)
    # Override parent method
    def getType(self):
        return Component.TYPE_EMITTER
    # TODO add component methods


#-----------------------------------
class GfxBurstEmitter(Gfx):

    # Constructor
    def __init__(self,params):
        # call to parent constructor
        super().__init__()
        # create Gfx element
        self.gfx = createParticleBurst(params)
    # Override parent method
    def getType(self):
        return Component.TYPE_BURST
    # TODO add component methods




