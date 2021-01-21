# TODO put single Sprite in a 1-size-spriteList to be more generic ?

## ============================================================
## IMPORTS
## ============================================================
import arcade



## ============================================================
## GFX MANAGER
## ============================================================
from ecs.components.gfx import Gfx


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
    ## Type checking
    ## -------------------------------------
    def __checkType(self, ref):
        if not isinstance(ref, Gfx):
            raise ValueError(f"[ERR] check gfx : bad object type. It should be Gfx !\n{ref}")


    ## -------------------------------------
    ## Draw List
    ## -------------------------------------
    def __addRefInDrawList(self, ref, type):
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

    def __clearDrawList(self):
        while len(self.drawList) > 0:
            self.drawList.remove(self.drawList[0])

    def __rebuildDrawList(self):
        print("Rebuild DRAW list")
        # prepare Sprite List to draw
        self.__clearDrawList()
        for row in self.gfxList:
            ref  = row[0]
            type = row[1]
            vis  = row[3]
            if vis:
                self.__addRefInDrawList(ref, type)


    ## -------------------------------------
    ## Gfx List
    ## -------------------------------------
    def __addEntryInGfxList(self, entry):
        gfx   = entry[0]
        zIdx  = entry[2]
        isVis = entry[3]
        # Search for the index to insert
        inserted = False
        for i in range(len(self.gfxList)):
            prevZ = self.gfxList[i][2]
            if prevZ < zIdx:
                # insert into list
                self.gfxList.insert(i, entry)
                inserted = True
                break
        # check for append
        if not inserted:
            self.gfxList.append(entry)
        # rebuild draw list
        self.__rebuildDrawList()


    ## -------------------------------------
    ## Register methods
    ## -------------------------------------
    def registerGfx(self, cmpRef, zIndex, isVisible=True):
        # check type
        self.__checkType(cmpRef)
        # get arcade gfx ref
        ref = cmpRef.getGfx()
        # prepare data
        data = [cmpRef.getType(), zIndex, isVisible, cmpRef]
        # add into the dictionary
        if ref in self.gfxDict:
            raise ValueError("[ERR] addAndSort : gfx already registered in the dict !")
        self.gfxDict[ref] = data
        # update Entry list
        self.__addEntryInGfxList([ref,] + data)
        pass

    def removeGfx(self, cmpRef):
        # get arcade gfx ref
        ref = cmpRef.getGfx()
        # No need to sort list when removing
        for row in self.gfxList:
            if ref == row[1]:
                self.gfxList.remove(row)
                return
        # Recompute draw list
        # TODO [PERF] :
        # just remove ref from the draw list instead of recreating a new one ?
        # may be not possible for particle emitters as we added a field of the ref ?
        # rebuild draw list
        self.__rebuildDrawList()


    ## -------------------------------------
    ## Main process methods
    ## -------------------------------------
    def updateAllGfx(self, deltaTime, isOnPause):
        # init list of gfx elements to remove
        ref2Remove = []
        # browse every gfx element and update
        for row in self.gfxList:
            ref    = row[0]
            type   = row[1]
            cmpRef = row[4]
            # Check pause behavior (no update if paused)
            if cmpRef.isEnabledOnPause() or (not isOnPause):
                # Animated sprites or spritelists
                if (type & Gfx.ANIMATED) == Gfx.ANIMATED:
                    # update animated sprites
                    ref.update_animation(deltaTime)
                # Particle emitters
                elif (type & Gfx.SIMPLE) != Gfx.SIMPLE:
                    # update particle emitters (normal or bursts)
                    ref.update(deltaTime)
                    # Remove burst emitters if finished
                    if type == Gfx.TYPE_BURST:
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


    # TODO : old version to rework !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
            for i in range(len(self.gfxList)):
                # found the reference in the list
                if self.gfxList[i][0] == ref:
                    # set new value
                    self.gfxList[i][3] = newVisible
                    # if the value is False, just remove ref from drawList (as it must be in the list
                    if not newVisible:
                        self.drawList.remove(ref)
                    else:
                        #TODO : how to add the ref at the correct index without recreating new List
                        self.__rebuildDrawList()
                    return
            # if we reached this statement, that means
            # the ref is not in the list but is in the dict
            raise ValueError("[ERR] setVisible : gfx not in the list but in the dict !!!")


