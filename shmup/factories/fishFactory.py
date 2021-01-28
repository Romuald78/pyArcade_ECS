import pymunk

from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite
from ecs.core.components.input import GamepadAxis
from ecs.core.components.physic import PhysicBox, PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.script.gfxpos import Follow
from ecs.user.script.phyuserscripts import GfxPhyLink, Move2DAnalogPhy, LimitBoxPhy
from shmup.common.constants import Z_INDEX_SHIPS, SCREEN_HEIGHT, SCREEN_WIDTH, COLLISION_PLAYER_MASK, ZIDX_CHARS, \
    COLLISION_FISH_MASK
from random import randint

from shmup.scripts.destroyFish import DestroyFish
from shmup.scripts.fishMove import FishMove


class FishFactory():

    FINAL_SIZE = 128

    def __init__(self):
        fs = FishFactory.FINAL_SIZE
        FISH01 = {"path": "resources/images/fishes/fish01.png",
                  "textureName":"fish01",
                  "size": (1280, 768),
                  "finalSize":(fs,fs),
                  "nbSprites": (5, 4),
                  "speed":5,
                  "period":1,
                  "amplitude":0
                  }
        FISH02 = {"path": "resources/images/fishes/fish02.png",
                  "textureName":"fish02",
                  "size": (512, 160),
                  "finalSize":(fs,fs),
                  "nbSprites": (2, 2),
                  "speed":9,
                  "period":1,
                  "amplitude":0
                  }
        FISH03 = {"path": "resources/images/fishes/fish03.png",
                  "textureName":"fish03",
                  "size": (1280, 480),
                  "finalSize":(fs,fs),
                  "nbSprites": (5, 4),
                  "speed":8,
                  "period":1,
                  "amplitude":0
                  }
        FISH04 = {"path": "resources/images/fishes/fish04.png",
                  "textureName":"fish04",
                  "size": (800, 1024),
                  "finalSize":(fs,fs),
                  "nbSprites": (4, 4),
                  "speed":2,
                  "period":1,
                  "amplitude":0
                  }
        JELLY  = {"path": "resources/images/fishes/jelly.png",
                  "textureName":"jelly",
                  "size": (800, 512),
                  "finalSize":(fs,fs),
                  "nbSprites": (5, 2),
                  "speed":2.5,
                  "period":2,
                  "amplitude":10
                  }
        LANTERN = {"path": "resources/images/fishes/lantern.png",
                   "textureName": "lantern",
                   "size": (1024, 800),
                  "finalSize":(fs,fs),
                   "nbSprites": (4, 4),
                   "speed":5,
                  "period":1,
                  "amplitude":5
                 }
        SQUID  = {"path": "resources/images/fishes/squid.png",
                  "textureName":"squid",
                 "size": (512, 192),
                  "finalSize":(fs,fs),
                 "nbSprites": (2, 3),
                  "speed":6,
                  "period":1,
                  "amplitude":1
                 }
        self._fishes = [
            FISH01,
            FISH02,
            FISH03,
            FISH04,
            JELLY,
            LANTERN,
            SQUID   ]


    def create(self, gfxFishList):

        # Create entity
        eFish = Entity("Fish")

        # Select random shape
        idx   = randint(0,len(self._fishes)-1)
        fish  = self._fishes[idx]
        nbX   = fish["nbSprites"][0]
        nbY   = fish["nbSprites"][1]
        W     = fish["size"][0] // nbX
        H     = fish["size"][1] // nbY
        fSize = fish["finalSize"]
        speed = fish["speed"]
        ampl  = fish["amplitude"]
        period= fish["period"]
        params = {
            "filePath": fish["path"],
            "textureName": fish["textureName"],
            "spriteBox": (nbX,nbY,W,H),
            "startIndex": 0,
            "endIndex": (W*H)-1,
            "frameDuration": 1 / 10,
            "size": fSize,
            "position":(SCREEN_WIDTH+(W//2),randint(H//2,SCREEN_HEIGHT-(H//2)))
        }
        fishGfx     = GfxAnimatedSprite(params, ZIDX_CHARS, "fishGfx")
        fishMove    = FishMove(fishGfx, speed, ampl, period)
        fishDestroy = DestroyFish(eFish, fishGfx, gfxFishList)

        # add all components to entity
        eFish.addComponent(fishGfx)
        eFish.addComponent(fishMove)
        eFish.addComponent(fishDestroy)

        # return result
        return eFish

