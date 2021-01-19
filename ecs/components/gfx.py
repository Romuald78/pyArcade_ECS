
## ============================================================
## IMPORTS
## ============================================================
from ecs.components.component import Component
from utils import *



## ============================================================
## GFX UPPER CLASS
## ============================================================
class Gfx(Component):

    # constructor
    def __init__(self, scn):
        self.scene = scn
        self.zIndex  = 0
        self.gfx     = None
        self.gfxType = None

    # arcade gfx object
    def getGfx(self):
        if self.gfx == None:
            raise ValueError("[ERR] gfx : gfx reference has not been set yet !")
        return self.gfx
    # type method
    def getType(self):
        if self.gfxType == None:
            raise ValueError("[ERR] gfx : gfxType reference has not been set yet !")
        return self.gfxType
    # Z-Index
    def getZIndex(self):
        return self.zIndex
    # Visible
    def setVisible(self,val):
        if self.gfxType == None:
            raise ValueError("[ERR] setVisible : gfxType reference has not been set yet !")
        self.scene.setVisible(self, val)
    def isVisible(self):
        if self.gfxType == None:
            raise ValueError("[ERR] getVisible : gfxType reference has not been set yet !")
        return self.scene.isVisible(self)



## ============================================================
## GFX COMPONENTS
## ============================================================

#-----------------------------------
class GfxOneSPrite(Gfx):

    # Constructor
    def __init__(self, scn):
        # call to parent constructor
        super().__init__(scn)

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
    def setScale(self, newScale):
        self.gfx.scale = newScale
    def getScale(self):
        return self.gfx.scale


#-----------------------------------
class GfxSimpleSprite(GfxOneSPrite):

    # Constructor
    def __init__(self, scn, params, zIdx=0):
        # call to parent constructor
        super().__init__(scn)
        # set type
        self.gfxType = Component.TYPE_SIMPLE_SPRITE
        # create Gfx element
        self.gfx     = createSimpleSprite(params)
        self.zIndex  = zIdx

#-----------------------------------
class GfxAnimatedSprite(GfxOneSPrite):

    # Constructor
    def __init__(self, scn, params, zIdx=0):
        # call to parent constructor
        super().__init__(scn)
        # set type
        self.gfxType = Component.TYPE_ANIM_SPRITE
        # create Gfx element
        self.gfx     = createAnimatedSprite(params)
        self.zIndex  = zIdx

#-----------------------------------
class GfxSimpleSpriteList(Gfx):

    # Constructor
    def __init__(self, scn, zIdx=0):
        # call to parent constructor
        super().__init__(scn)
        # create Gfx element
        self.gfx = arcade.SpriteList()
        self.zIndex = zIdx

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




