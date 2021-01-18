
## ============================================================
## GFX GENERIC INTERFACE
## ============================================================
from utils import *


class Gfx():

    ## -------------------------------------
    ## Types
    ## -------------------------------------
    SIMPLE    = 0x01
    ANIMATED  = 0x02
    UNLIMITED = 0x03
    LIMITED   = 0x04

    SINGLE    = 0x10
    LIST      = 0x20
    PARTICLES = 0x40

    SIMPLE_SPRITE   = SIMPLE    | SINGLE
    ANIMATED_SPRITE = ANIMATED  | SINGLE
    SIMPLE_LIST     = SIMPLE | LIST
    ANIMATED_LIST   = ANIMATED  | LIST
    NORMAL_EMITTER  = UNLIMITED | PARTICLES
    BURST_EMITTER   = LIMITED   | PARTICLES

    # Get arcade gfx object
    def getGfx(self):
        raise ValueError("[ERR] gfx : getGfx todo method seems to be not implemented !\nMay be your gfx object does not have the correct type !")

    # generic method
    def getType(self):
        raise ValueError("[ERR] gfx : getType todo method has not been implemented yet !")



## ============================================================
## GFX COMPONENTS
## ============================================================

class GfxSimpleSprite(Gfx):
    def __init__(self,params):
        self.gfx = createSimpleSprite(params)
    def getType(self):
        return Gfx.SIMPLE_SPRITE

class GfxAnimatedSprite(Gfx):
    def __init__(self,params):
        self.gfx = createAnimatedSprite(params)
    def getType(self):
        return Gfx.ANIMATED_SPRITE

class GfxSimpleSpriteList(Gfx):
    def __init__(self):
        self.gfx = arcade.SpriteList()
    def addSprite(self, params):
        newSprite = createSimpleSprite(params)
        self.gfx.append(newSprite)
    def getType(self):
        return Gfx.SIMPLE_LIST

class GfxAnimatedSpriteList(Gfx):
    def __init__(self):
        self.gfx = arcade.SpriteList()
    def addSprite(self, params):
        newSprite = createAnimatedSprite(params)
        self.gfx.append(newSprite)
    def getType(self):
        return Gfx.ANIMATED_LIST

class GfxSimpleEmitter(Gfx):
    def __init__(self, params):
        self.gfx = createParticleEmitter(params)
    def getType(self):
        return Gfx.NORMAL_EMITTER

class GfxBurstEmitter(Gfx):
    def __init__(self,params):
        self.gfx = createParticleBurst(params)
    def getType(self):
        return Gfx.BURST_EMITTER


