# FEATURE : Merge gfx classes
# put a single Sprite in a 1-size-spriteList
# to be more generic ? We would only have GfxSpriteList
# that would be easier to handle in GfxSystem class. let's see


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
    def __init__(self, scn, compName=None):
        if compName==None:
            compName = "GFX"
        super().__init__(compName)
        self._scene     = scn
        self._zIndex    = 0
        self._arcadeGfx = None
        self._gfxType   = None
        self._visible   = True

    # arcade gfx object
    def getGfx(self):
        if self._arcadeGfx == None:
            raise ValueError("[ERR] gfx : arcade gfx reference has not been set yet !")
        return self._arcadeGfx
    # type method
    def getType(self):
        if self._gfxType == None:
            raise ValueError("[ERR] gfx : gfxType reference has not been set yet !")
        return self._gfxType
    # Z-Index
    def setZIndex(self, newZ):
        self._zIndex = newZ
        self._scene.notifyUpdateZIndex(self)
    def getZIndex(self):
        return self._zIndex
    # Visible (set the component field + notify Gfx Manager in order to update the draw list
    def show(self):
        self._visible = True
        self._scene.notifyUpdateVisible(self)
    def hide(self):
        self._visible = False
        self._scene.notifyUpdateVisible(self)
    def isVisible(self):
        return self._visible



## ============================================================
## GFX COMPONENTS
## ============================================================

#-----------------------------------
class GfxOneSPrite(Gfx):

    # Constructor
    def __init__(self, scn, compName=None):
        if compName == None:
            compName = "1SPRITE"
        # call to parent constructor
        super().__init__(scn, compName)

    # Position
    def move(self, dx, dy):
        self._arcadeGfx.center_x += dx
        self._arcadeGfx.center_y += dy
    def setPosition(self, newPos):
        self._arcadeGfx.center_x = newPos[0]
        self._arcadeGfx.center_y = newPos[1]
    def getPosition(self):
        return (self._arcadeGfx.center_x, self._arcadeGfx.center_y)

    # Orientation
    # QUESTION : is there a problem not to be in a specific range like [0-360] or [-180-180] ?
    # FEATURE  : improve methods to handle pivot points
    def rotate(self, offset, multiplier=1.0, pivotPos=None):
        self._arcadeGfx.angle *= multiplier
        self._arcadeGfx.angle += offset
    def setAngle(self, newAngle, pivotPos=None):
        self._arcadeGfx.angle = newAngle
    def getAngle(self):
        return self._arcadeGfx.angle

    # Scale
    def setScale(self, newScale):
        self._arcadeGfx.scale = newScale
    def getScale(self):
        return self._arcadeGfx.scale

#-----------------------------------
class GfxSimpleSprite(GfxOneSPrite):

    # Constructor
    def __init__(self, scn, params, zIdx=0, compName=None):
        if compName == None:
            compName = "FixedSPrite"
        # call to parent constructor
        super().__init__(scn,compName)
        # set type
        self._gfxType   = Component.TYPE_SIMPLE_SPRITE
        # create Gfx element
        self._arcadeGfx = createSimpleSprite(params)
        self._zIndex    = zIdx

#-----------------------------------
class GfxAnimatedSprite(GfxOneSPrite):

    # Constructor
    def __init__(self, scn, params, zIdx=0, compName=None):
        if compName == None:
            compName = "AnimSPrite"
        # call to parent constructor
        super().__init__(scn,compName)
        # set type
        self._gfxType   = Component.TYPE_ANIM_SPRITE
        # create Gfx element
        self._arcadeGfx = createAnimatedSprite(params)
        self._zIndex    = zIdx



#-----------------------------------
class GfxSpriteList(Gfx):

    # Constructor
    def __init__(self, scn, compName=None):
        if compName == None:
            compName = "SPRITELIST"
        # call to parent constructor
        super().__init__(scn, compName)

    # Filling
    def addSprite(self, params):
        raise ValueError("[ERR] GfxSPriteList - add : this method has not been implemented yet !")

    # Position
    def move(self, dx, dy):
        for gfx in self._arcadeGfx:
            gfx.center_x += dx
            gfx.center_y += dy

    # Orientation
    def rotate(self, offset, mult=1, pivotPos=None):
        for gfx in self._arcadeGfx:
            gfx.angle *= mult
            gfx.angle += offset

    # List management
    def size(self):
        return len(self._arcadeGfx)
    def getSprite(self,index):
        return self._arcadeGfx[index]

#-----------------------------------
class GfxSimpleSpriteList(GfxSpriteList):

    # Constructor
    def __init__(self, scn, zIdx=0, compName=None):
        if compName == None:
            compName = "FixedList"
        # call to parent constructor
        super().__init__(scn,compName)
        # set type
        self._gfxType   = Component.TYPE_SIMPLE_SPRITE
        # create Gfx element
        self._arcadeGfx = arcade.SpriteList()
        self._zIndex = zIdx

    # Override parent method
    def addSprite(self, params):
        newSprite = createSimpleSprite(params)
        self._arcadeGfx.append(newSprite)

#-----------------------------------
class GfxAnimatedSpriteList(GfxSpriteList):

    def __init__(self, scn, zIdx=0, compName=None):
        if compName == None:
            compName = "AnimList"
        # call to parent constructor
        super().__init__(scn,compName)
        # set type
        self._gfxType   = Component.TYPE_SIMPLE_SPRITE
        # create Gfx element
        self._arcadeGfx = arcade.SpriteList()
        self._zIndex    = zIdx

    # Override parent method
    def addSprite(self, params):
        newSprite = createAnimatedSprite(params)
        self._arcadeGfx.append(newSprite)



#-----------------------------------
class GfxSimpleEmitter(Gfx):

    def __init__(self, scn, params, zIdx=0, compName=None):
        if compName == None:
            compName = "Emitter"
        # call to parent constructor
        super().__init__(scn,compName)
        # set type
        self._gfxType   = Component.TYPE_EMITTER
        # create Gfx element
        self._arcadeGfx = createParticleEmitter(params)
        self._zIndex    = zIdx

    # position
    def move(self, dx, dy):
        self._arcadeGfx.center_x += dx
        self._arcadeGfx.center_y += dy
    def setPosition(self, newPos):
        self._arcadeGfx.center_x = newPos[0]
        self._arcadeGfx.center_y = newPos[1]
    def getPosition(self):
        return (self._arcadeGfx.center_x, self._arcadeGfx.center_y)

#-----------------------------------
class GfxBurstEmitter(Gfx):

    def __init__(self, scn, params, zIdx=0, compName=None):
        if compName == None:
            compName = "Burst"
        # call to parent constructor
        super().__init__(scn,compName)
        # set type
        self._gfxType   = Component.TYPE_BURST
        # create Gfx element
        self._arcadeGfx = createParticleBurst(params)
        self._zIndex    = zIdx

    # position
    def move(self, dx, dy):
        self._arcadeGfx.center_x += dx
        self._arcadeGfx.center_y += dy
    def setPosition(self, newPos):
        self._arcadeGfx.center_x = newPos[0]
        self._arcadeGfx.center_y = newPos[1]
    def getPosition(self):
        return (self._arcadeGfx.center_x, self._arcadeGfx.center_y)

