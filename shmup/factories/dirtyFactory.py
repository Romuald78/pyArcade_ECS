from random import randint

import pymunk

from ecs.core.components.gfx import GfxAnimatedSprite
from ecs.core.components.light import LightFx
from ecs.core.components.physic import PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.script.gfxpos import LightFollowGfx
from ecs.user.script.phyuserscripts import PhyGfxLink
from shmup.common.constants import ZIDX_COINS, COLL_TYPE_COIN, COLL_TYPE_DIRTY
from shmup.components.dirttype import DirtType
from shmup.scripts.movecoin import MoveCoin


class DirtyFactory():

    DIRTS = [
        {
            "filePath": f"resources/images/items/shoe.png",
            "size": (128, 128),
            "textureName": f"shoe",
            "spriteBox": (1, 1, 128, 128),
        },
        {
            "filePath": f"resources/images/items/can.png",
            "size": (128, 128),
            "textureName": f"can",
            "spriteBox": (1, 1, 128, 128),
        },
        {
            "filePath": f"resources/images/items/tyre.png",
            "size": (128, 128),
            "textureName": f"can",
            "spriteBox": (1, 1, 128, 128),
        }
    ]

    def __init__(self):
        pass

    def create(self, type, position, eDirty):
        dirty = Entity()
        params = {
            "position": position,
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1,
            "counter": 0,
            "backAndForth": False
        }
        data = DirtyFactory.DIRTS[type]
        for key in data:
            params[key] = data[key]
        limitY = randint(90,200)
        dirtyGfx = GfxAnimatedSprite(params, ZIDX_COINS+limitY-90)
        dirtyGfx.angle = randint(-100,100)/10
        speed =randint(100,400)/100
        moveDirty = MoveCoin(dirtyGfx, limitY, 20, position, eDirty, speed)
        params = {
            "mass": 0.01,
            "radius": 64,
            "mode": pymunk.Body.KINEMATIC,
            "pos": (10000, 10000),
            "sensor": False,
            "collisionType": COLL_TYPE_DIRTY,
        }
        dirtyPhy = PhysicDisc(params, "dirtyPhy")
        phyGfxLink = PhyGfxLink(dirtyPhy, dirtyGfx, (0,0), "phygfxlink")

        # light
        light = LightFx((-1000,-1000),64,(255,16,0),"soft")
        lightFollow = LightFollowGfx(dirtyGfx, light, None)

        # Type
        typeCmp = DirtType(type,"dirtType")

        dirty.addComponent(dirtyGfx)
        dirty.addComponent(moveDirty)
        dirty.addComponent(dirtyPhy)
        dirty.addComponent(phyGfxLink)
        dirty.addComponent(light)
        dirty.addComponent(lightFollow)
        dirty.addComponent(typeCmp)

        # return entity
        return dirty
