from random import randint

import pymunk

from ecs.core.components.gfx import GfxAnimatedSprite
from ecs.core.components.light import LightFx
from ecs.core.components.physic import PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.script.gfxpos import LightFollowGfx
from ecs.user.script.phyuserscripts import PhyGfxLink
from shmup.common.constants import ZIDX_COINS, COLL_TYPE_COIN
from shmup.scripts.movecoin import MoveCoin


class CoinFactory():


    def __init__(self):
        pass

    def create(self, position, eCoins):
        coin = Entity()
        params = {
            "filePath": f"resources/images/items/coins.png",
            "size": (64, 64),
            "position": position,
            "textureName": f"coin",
            "spriteBox": (3, 2, 128, 128),
            "startIndex": 0,
            "endIndex": 5,
            "frameDuration": 1 / 20,
            "counter": 0,
            "backAndForth": False
        }
        limitY = randint(90,200)
        coinGfx = GfxAnimatedSprite(params, ZIDX_COINS+limitY-90)
        moveCoin = MoveCoin(coinGfx, limitY, 20, position, eCoins)
        params = {
            "mass": 0.01,
            "radius": 32,
            "mode": pymunk.Body.KINEMATIC,
            "pos": (10000, 10000),
            "sensor": False,
            "collisionType": COLL_TYPE_COIN,
        }
        coinPhy = PhysicDisc(params, "coinPhy")
        phyGfxLink = PhyGfxLink(coinPhy, coinGfx, (0,0), "phygfxlink")

        # light
        light = LightFx((-1000,-1000),48,(255,255,0),"soft")
        lightFollow = LightFollowGfx(coinGfx, light, None)


        coin.addComponent(coinGfx)
        coin.addComponent(moveCoin)
        coin.addComponent(coinPhy)
        coin.addComponent(phyGfxLink)
        coin.addComponent(light)
        coin.addComponent(lightFollow)


        # return entity
        return coin