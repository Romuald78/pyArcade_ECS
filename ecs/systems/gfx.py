# TODO put single Sprite in a 1-size-spriteList to be more generic ?

## ============================================================
## IMPORTS
## ============================================================
import arcade



## ============================================================
## GFX MANAGER
## ============================================================
from ecs.todo.gfx import Gfx


class GfxSystem():

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self):
        # list contains all information
        # sorted by visible first,
        # by Z-index then (decreasing order)
        self.gfxList = []
        # dict contains all information too
        # and is used for getter methods (faster)
        self.gfxDict = {}
        self.drawList = arcade.SpriteList()


    ## -------------------------------------
    ## Private methods
    ## -------------------------------------
    def __checkType(self, ref):
        if not isinstance(ref, Gfx):
            raise ValueError(f"[ERR] check gfx : bad object type. It should be Gfx !\n{ref}")

    def __fillDrawList(self):
        # prepare Sprite List to draw
        self.drawList = arcade.SpriteList()
        for row in self.gfxList:
            ref  = row[0]
            type = row[1]
            vis  = row[3]
            if vis:
                if (type & Gfx.SINGLE) == Gfx.SINGLE:
                    # Add single sprite to draw list
                    self.drawList.append(ref)
                elif (type & Gfx.LIST) == Gfx.LIST:
                    # add sprite list to draw list
                    self.drawList.extend(ref)
                elif (type & Gfx.PARTICLES) == Gfx.PARTICLES:
                    # add all particles of emitter
                    # TODO : check if it works to get the particle spriteList from an emitter ??
                    self.drawList.extend(ref._particles)
                    raise ValueError("[TODO] particle emitters are not handled yet in the GFX system !")
            else:
                # the list is sorted so , if we reached a False
                # value in the "visible" property, that means
                # there is no mre gfx to display
                break

    def __sortOnly(self):
        # sort the list
        self.gfxList = sorted(self.gfxList, key=lambda x: (-x[3], -x[2]))
        # Update draw list
        self.__fillDrawList()

    def __addAndSort(self, ref, data):
        # add into the dictionary
        if ref in self.gfxDict:
            raise ValueError("[ERR] addAndSort : gfx already registered in the dict !")
        self.gfxDict[ref] = data
        # Add into the list
        self.gfxList.append([ref, ] + data)
        # sort the list
        self.__sortOnly()


    ## -------------------------------------
    ## Register methods
    ## -------------------------------------
    def registerGfx(self, cmpRef, zIndex, isVisible=True):
        # check type
        self.__checkType(cmpRef)
        # get arcade gfx ref
        gfxRef = cmpRef.getGfx()
        # prepare data
        data = [cmpRef.getType(), zIndex, isVisible]
        # add data and sort gfx lists
        self.__addAndSort(gfxRef, data)

#    def registerFixedSprite(self, ref, zIndex, isVisible=True):
#        data = [GfxInterface.FIXED_SPRITE, zIndex, isVisible]
#        self.__addAndSort(ref, data)

#    def registerFixedSpriteList(self, ref, zIndex, isVisible=True):
#        data = [GfxInterface.FIXED_LIST, zIndex, isVisible]
#        self.__addAndSort(ref, data)

#    def registerAnimatedSprite(self, ref, zIndex, isVisible=True):
#        data = [GfxInterface.ANIMATED_SPRITE, zIndex, isVisible]
#        self.__addAndSort(ref, data)

#    def registerAnimatedSpriteList(self, ref, zIndex, isVisible=True):
#        data = [GfxInterface.ANIMATED_LIST, zIndex, isVisible]
#        self.__addAndSort(ref, data)

#    def registerParticleEmitter(self, ref, zIndex, isVisible=True):
#        data = [GfxInterface.SIMPLE_EMITTER, zIndex, isVisible]
#        self.__addAndSort(ref, data)

#    def registerParticleBurst(self, ref, zIndex, isVisible=True):
#        data = [GfxInterface.BURST_EMITTER, zIndex, isVisible]
#        self.__addAndSort(ref, data)

    def removeGfx(self, ref):
        # No need to sort list when removing
        for row in self.gfxList:
            if ref == row[1]:
                self.gfxList.remove(row)
                return
        # Recompute draw list
        # TODO [PERF] :
        # just remove ref from the draw list instead of recreating a new one ?
        # may be not possible for particle emitters as we added a field of the ref ?
        self.__fillDrawList()


    ## -------------------------------------
    ## Main process methods
    ## -------------------------------------
    def updateAllGfx(self, deltaTime):
        # init list of gfx elements to remove
        ref2Remove = []
        # browse every gfx element and update
        for row in self.gfxList:
            ref  = row[0]
            type = row[1]
            if (type & Gfx.ANIMATED) == Gfx.ANIMATED:
                # update animated sprites
                ref.update_animation(deltaTime)
            elif (type & Gfx.SIMPLE) != Gfx.SIMPLE:
                # update particle emitters (normal or bursts)
                ref.update(deltaTime)
                # Remove burst id finished
                if type == Gfx.BURST_EMITTER:
                    if ref.can_reap():
                        ref2Remove.append(ref)
        # remove useless gfx elements
        for ref in ref2Remove:
            self.removeGfx(ref)

    def drawAllGfx(self):
        self.drawList.draw()


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
        # update only if we change the value
        if self.gfxDict[ref][1] != newZ:
            # update dict
            self.gfxDict[ref][1] = newZ
            # update list
            for g in self.gfxList:
                if g[0] == ref:
                    g[2] = newZ
                    # update is done, now sort lists
                    self.__sortOnly()
                    # just exit process
                    return
            raise ValueError("[ERR] setZIndex : gfx not in the list !")

    def setVisible(self, ref, newVisible):
        # update dictionary
        if ref not in self.gfxDict:
            raise ValueError("[ERR] setVisible : gfx not in the dict !")
        # update only if we change the value
        if self.gfxDict[ref][2] != newVisible:
            # update dict
            self.gfxDict[ref][2] = newVisible
            # update list
            for g in self.gfxList:
                if g[0] == ref:
                    g[3] = newVisible
                    # update is done, now sort lists
                    self.__sortOnly()
                    # just exit process
                    return
            # if we reached this statement, that means
            # the ref is not in the list but is in the dict
            raise ValueError("[ERR] setVisible : gfx not in the list but in the dict !!!")


