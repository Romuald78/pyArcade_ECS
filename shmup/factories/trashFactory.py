from random import randint

import arcade

from ecs.core.components.gfx import GfxAnimatedSprite, GfxMultiSprite
from ecs.core.components.input import Keyboard
from ecs.core.main.entity import Entity
from ecs.user.idle.counters import UserCounter
from shmup.common.constants import ZIDX_COINS, ZIDX_HUD, SCREEN_WIDTH, SCREEN_HEIGHT
from shmup.scripts.chest import Chest
from shmup.scripts.movecoin import MoveCoin
from shmup.scripts.trash import Trash
from shmup.scripts.updatescores import UpdateScores


class TrashFactory():


    def __init__(self):
        pass

    def create(self, position):
        trash = Entity()
        trashGfx = GfxAnimatedSprite(None, ZIDX_HUD)
        params = {
            "filePath": f"resources/images/items/trash.png",
            "size": (128, 384//2),
            "position": position,
            "animName": f"close",
            "spriteBox": (5, 1, 256, 384),
            "startIndex": 4,
            "endIndex": 0,
            "frameDuration": 1 / 30,
            "counter": 1,
            "backAndForth": False
        }
        trashGfx.addAnimation(params,True,True)
        params = {
            "filePath": f"resources/images/items/trash.png",
            "size": (256, 384),
            "position": position,
            "animName": f"open",
            "spriteBox": (5, 1, 256, 384),
            "startIndex": 0,
            "endIndex": 4,
            "frameDuration": 1 / 30,
            "counter": 1,
            "backAndForth": False
        }
        trashGfx.addAnimation(params)

        # score
        score = UserCounter(0,1000000,0)

        # Gfx for score + script
        refX = position[0]+64
        refY = position[1]-32
        w = 80
        h = 128
        ratio = 0.4
        params = {
            "animName": f"digit",
            "counter": 0,
            "backAndForth": False,
            "filePath": "resources/images/hud/numbers.png",
            "spriteBox": (10, 1, w, h),
            "startIndex": 0,
            "endIndex": 9,
            "frameDuration": 1 / 10,
            "size": (int(w*ratio),int(h*ratio)),
            "position": (refX,refY)
        }
        thousandGfx = GfxAnimatedSprite(params, ZIDX_HUD-1, "thousandGfx")

        refX += (w)*ratio
        refY += 0
        params["size"] = (int(w*ratio),int(h*ratio))
        params["position"] = (refX,refY)
        hundredGfx = GfxAnimatedSprite(params, ZIDX_HUD-1, "hundredGfx")

        refX += (w)*ratio
        refY += 0
        params["size"] = (int(w*ratio),int(h*ratio))
        params["position"] = (refX,refY)
        decadeGfx = GfxAnimatedSprite(params, ZIDX_HUD-1, "decadeGfx")

        refX += (w)*ratio
        refY += 0
        params["size"] = (int(w*ratio),int(h*ratio))
        params["position"] = (refX,refY)
        unitGfx = GfxAnimatedSprite(params, ZIDX_HUD-1, "unitGfx")

        # Create score update script
        scrUpdate = UpdateScores(score,unitGfx, decadeGfx, hundredGfx, thousandGfx)

        # Script to handle coin gathering
        openClose = Trash(trashGfx,score,position,"trashScr")

        trash.addComponent(trashGfx)
        trash.addComponent(openClose)
        trash.addComponent(score)
        trash.addComponent(unitGfx)
        trash.addComponent(decadeGfx)
        trash.addComponent(hundredGfx)
        trash.addComponent(thousandGfx)
        trash.addComponent(scrUpdate)

        # return entity
        return trash