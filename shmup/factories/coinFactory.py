from random import randint

from ecs.core.components.gfx import GfxAnimatedSprite
from ecs.core.main.entity import Entity
from shmup.common.constants import ZIDX_COINS
from shmup.scripts.movecoin import MoveCoin


class CoinFactory():


    def __init__(self):
        pass

    def create(self, position):
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
        moveCoin = MoveCoin(coinGfx, limitY, 20, position)

        coin.addComponent(coinGfx)
        coin.addComponent(moveCoin)

        # return entity
        return coin