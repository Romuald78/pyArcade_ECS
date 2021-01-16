## ============================================================
## IMPORTS
## ============================================================
import arcade
import time


## ============================================================
## GFX MANAGER
## ============================================================
class GfxManager():

    ## -------------------------------------
    ## Types
    ## -------------------------------------
    FIXED     = 0x01
    ANIMATED  = 0x02
    UNLIMITED = 0x03
    LIMITED   = 0x04
    SINGLE    = 0x10
    LIST      = 0x20
    PARTICLES = 0x40
    FIXED_SPRITE    = FIXED     | SINGLE
    ANIMATED_SPRITE = ANIMATED  | SINGLE
    FIXED_LIST      = FIXED     | LIST
    ANIMATED_LIST   = ANIMATED  | LIST
    EMITTER         = UNLIMITED | PARTICLES
    BURST           = LIMITED   | PARTICLES


    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self):
        self.gfxList = []
        self.gfxDict = {}
        self.drawList = arcade.SpriteList()


    ## -------------------------------------
    ## Register methods
    ## -------------------------------------
    def __addAndSort(self, ref, data):
        # add into the dictionary
        if ref in self.gfxDict:
            raise ValueError("[ERR] addAndSort : gfx already registered in the dict !")
        self.gfxDict[ref] = data
        # Add into the list
        self.gfxList.append([ref,]+data)
        # sort the list
        self.gfxList = sorted(self.gfxList, key=lambda x: (-x[3], -x[2]))

    def registerFixedSprite(self, ref, zIndex, isVisible=True):
        data = [GfxManager.FIXED_SPRITE, zIndex, isVisible]
        self.__addAndSort(ref, data)

    def registerFixedSpriteList(self, ref, zIndex, isVisible=True):
        data = [GfxManager.FIXED_LIST, zIndex, isVisible]
        self.__addAndSort(ref, data)

    def registerAnimatedSprite(self, ref, zIndex, isVisible=True):
        data = [GfxManager.ANIMATED_SPRITE, zIndex, isVisible]
        self.__addAndSort(ref, data)

    def registerAnimatedSpriteList(self, ref, zIndex, isVisible=True):
        data = [GfxManager.ANIMATED_LIST, zIndex, isVisible]
        self.__addAndSort(ref, data)

    def registerParticleEmitter(self, ref, zIndex, isVisible=True):
        data = [GfxManager.EMITTER, zIndex, isVisible]
        self.__addAndSort(ref, data)

    def registerParticleBurst(self, ref, zIndex, isVisible=True):
        data = [GfxManager.BURST, zIndex, isVisible]
        self.__addAndSort(ref, data)

    def remove(self, ref):
        # No need to sort list when removing
        for row in self.gfxList:
            if ref == row[1]:
                self.gfxList.remove(row)
                return


    ## -------------------------------------
    ## Main process methods
    ## -------------------------------------
    def updateAllGfx(self, deltaTime):
#        measure = time.time()
        # init list of gfx elements to remove
        ref2Remove = []
        # browse every gfx element and update
        for row in self.gfxList:
            ref  = row[0]
            type = row[1]
            if (type & GfxManager.ANIMATED) == GfxManager.ANIMATED:
                # update animated sprites
                ref.update_animation(deltaTime)
            elif (type & GfxManager.FIXED) != GfxManager.FIXED:
                # update particle emitters (normal or bursts)
                ref.update(deltaTime)
                # Remove burst id finished
                if type == GfxManager.BURST:
                    if ref.can_reap():
                        ref2Remove.append(ref)
        # remove useless gfx elements
        for ref in ref2Remove:
            self.remove(ref)
#        measure = time.time()-measure
#        print(f"UPDATE GFX = {measure}")

    def drawAllGfx(self):
#        measure = time.time()
        # prepare Sprite List to draw
        self.drawList = arcade.SpriteList()
        for row in self.gfxList:
            ref  = row[0]
            type = row[1]
            vis  = row[3]
            if vis:
                if (type & GfxManager.SINGLE) == GfxManager.SINGLE:
                    # Add single sprite to draw list
                    self.drawList.append(ref)
                elif (type & GfxManager.LIST) == GfxManager.LIST:
                    # add sprite list to draw list
                    self.drawList.extend(ref)
                elif (type & GfxManager.PARTICLES) == GfxManager.PARTICLES:
                    # add all particles of emitter [TODO] not sure it works : to be tested !!
                    self.drawList.extend(ref._particles)
            else:
                # the list is sorted so , if we reached a False
                # value in the "visible" property, that means
                # there is no mre gfx to display
                break
        # Draw the prepared list
        self.drawList.draw()
#        measure = time.time()-measure
#        print(f"UPDATE DRW = {measure}")


    ## -------------------------------------
    ## Setters / Getters
    ## -------------------------------------
    def getType(self, ref):
        if ref not in self.gfxDict:
            raise ValueError("[ERR] getType : gfx not in the dict !")
        return self.gfxDict[ref][0]

    def getZIndex(self, ref):
        if ref not in self.gfxDict:
            raise ValueError("[ERR] getZIndex : gfx not in the dict !")
        return self.gfxDict[ref][1]

    def isVisible(self, ref):
        if ref not in self.gfxDict:
            raise ValueError("[ERR] isVisible : gfx not in the dict !")
        return self.gfxDict[ref][2]

    def setZIndex(self, ref, newZ):
        # update dictionary
        if ref not in self.gfxDict:
            raise ValueError("[ERR] setZIndex : gfx not in the dict !")
        self.gfxDict[ref][1] = newZ
        for g in self.gfxList:
            if g[0] == ref:
                g[2] = newZ
                return
        raise ValueError("[ERR] setZIndex : gfx not in the list !")

    def setVisible(self, ref, newVisible):
        # update dictionary
        if ref not in self.gfxDict:
            raise ValueError("[ERR] setVisible : gfx not in the dict !")
        self.gfxDict[ref][2] = newVisible
        for g in self.gfxList:
            if g[0] == ref:
                g[3] = newVisible
                return
        raise ValueError("[ERR] setVisible : gfx not in the list !")


