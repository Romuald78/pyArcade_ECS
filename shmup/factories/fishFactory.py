import pymunk

from ecs.core.components.gfx import GfxAnimatedSprite
from ecs.core.components.physic import PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.idle.counters import UserCounter
from ecs.user.script.phyuserscripts import PhyGfxLink
from shmup.common.constants import *
from random import randint

from shmup.scripts.destroyFish import DestroyFish
from shmup.scripts.fishMove import FishMove


class FishFactory():

    FINAL_SIZE = 128

    def __init__(self, gfxFishList, entFishList):
        self._gfxFishList = gfxFishList
        self._entFishList = entFishList

        fs = FishFactory.FINAL_SIZE
        FISH01 = {"path": "resources/images/fishes/fish01.png",
                  "textureName":"fish01",
                  "size": (1280, 768),
                  "finalSize":(1.30*fs,1.30*fs),
                  "phyRadius": (fs // 2) * 0.85,
                  "nbSprites": (5, 4),
                  "speed":5,
                  "period":1,
                  "amplitude":0,
                  "offset":(-8,0),
                  "life":5
                  }
        FISH02 = {"path": "resources/images/fishes/fish02.png",
                  "textureName":"fish02",
                  "size": (512, 160),
                  "finalSize":(3*fs,3*fs),
                  "phyRadius": (fs // 2) * 0.8,
                  "nbSprites": (2, 2),
                  "speed":9,
                  "period":1,
                  "amplitude":0,
                  "offset":(-96,0),
                  "life":3
                  }
        FISH03 = {"path": "resources/images/fishes/fish03.png",
                  "textureName":"fish03",
                  "size": (1280, 480),
                  "finalSize":(2*fs,2*fs),
                  "phyRadius": (fs // 2) * 0.85,
                  "nbSprites": (5, 4),
                  "speed":8,
                  "period":1,
                  "amplitude":0,
                  "offset":(-64,0),
                  "life":1
                  }
        FISH04 = {"path": "resources/images/fishes/fish04.png",
                  "textureName":"fish04",
                  "size": (800, 1024),
                  "finalSize":(1.3*fs,1.3*fs),
                  "phyRadius": (fs // 2) * 0.85,
                  "nbSprites": (4, 4),
                  "speed":2,
                  "period":1,
                  "amplitude":0,
                  "offset":(0,0),
                  "life":6
                  }
        JELLY  = {"path": "resources/images/fishes/jelly.png",
                  "textureName":"jelly",
                  "size": (800, 512),
                  "finalSize":(1.7*fs,1.7*fs),
                  "phyRadius": (fs // 2) * 0.7,
                  "nbSprites": (5, 2),
                  "speed":2.5,
                  "period":2,
                  "amplitude":10,
                  "offset":(0,64),
                  "life":3
                  }
        LANTERN = {"path": "resources/images/fishes/lantern.png",
                   "textureName": "lantern",
                   "size": (1024, 800),
                  "finalSize":(1.6*fs,1.6*fs),
                   "phyRadius":(fs//2)*0.85,
                   "nbSprites": (4, 4),
                   "speed":5,
                  "period":1,
                  "amplitude":5,
                  "offset":(-8,-8),
                  "life":4
                 }
        SQUID  = {"path": "resources/images/fishes/squid.png",
                  "textureName":"squid",
                 "size": (512, 192),
                  "finalSize":(3*fs,3*fs),
                  "phyRadius": (fs // 2) * 0.85,
                  "nbSprites": (2, 3),
                  "speed":6,
                  "period":1,
                  "amplitude":2.5,
                  "offset":(-64,0),
                  "life":4
                 }
        self._fishes = [
            FISH01,
            FISH02,
            FISH03,
            FISH04,
            JELLY,
            LANTERN,
            SQUID   ]


    def create(self):

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
        phyRadius = fish["phyRadius"]
        speed = fish["speed"]
        ampl  = fish["amplitude"]
        period= fish["period"]
        offset= fish["offset"]
        life = fish["life"]
        params = {
            "filePath": fish["path"],
            "textureName": fish["textureName"],
            "spriteBox": (nbX,nbY,W,H),
            "startIndex": 0,
            "endIndex": (W*H)-1,
            "frameDuration": 1 / 10,
            "size": fSize,
            "position":(SCREEN_WIDTH+(W//2),randint(H//2+100,SCREEN_HEIGHT-(H//2)-100)),
        }
        fishGfx     = GfxAnimatedSprite(params, ZIDX_FISHES, "fishGfx")
        fishMove    = FishMove(fishGfx, speed, ampl, period)
        fishDestroy = DestroyFish(eFish, fishGfx, self._gfxFishList, self._entFishList)

        params = {
            "mass"         : 0.01,
            "radius"       : phyRadius,
            "mode"         : pymunk.Body.KINEMATIC,
            "pos"          : (10000,10000),
            "sensor"       : False,
            "collisionType": COLL_TYPE_FISH,
        }
        fishPhy = PhysicDisc(params,"fishPhy")
        phyGfxLink = PhyGfxLink(fishPhy, fishGfx, offset, "phygfxlink")

        # Player life
        lifeCmp = UserCounter(0, life, life, True, "fishLife")

        # add all components to entity
        eFish.addComponent(fishGfx)
        eFish.addComponent(fishMove)
        eFish.addComponent(fishDestroy)
        eFish.addComponent(fishPhy)
        eFish.addComponent(phyGfxLink)
        eFish.addComponent(lifeCmp)

        # return result
        return eFish

