import arcade
from random import *

from ecs.components.gfx import GfxSimpleSpriteList
from ecs.main.entity import Entity

class GrassFactory():

    def __init__(self, scn):
        self.scene  = scn

    def create(self, refX, refY, refW, zIndex, grassW, grassH, clrFilter=(255,255,255)):
        # Create entity
        entity = Entity()
        # Create GfxSpriteList
        lst = GfxSimpleSpriteList(zIndex)
        # Create all sprite using param structure
        for i in range(refW // grassW):
            params = {
                "filePath": f"images/grass.png",
                "size": (grassW, grassH),
                "position": ((i * grassW) + randint(0, grassW//2) - (grassW//4) + refX, refY),
                "filterColor": clrFilter
            }
            if random() >= 0.3:
                params["flipH"] = True
            lst.addSprite(params)
        # Add sprite list gfx into entity
        entity.addComponent("Grass", lst)

        # return result
        return entity
