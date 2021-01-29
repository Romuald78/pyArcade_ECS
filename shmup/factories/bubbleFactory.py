import pymunk

from ecs.core.components.gfx import GfxAnimatedSprite
from ecs.core.components.physic import PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.script.phyuserscripts import PhyGfxLink, GfxPhyLink
from shmup.common.constants import *
from random import randint

from shmup.scripts.bubbleMove import BubbleMove
from shmup.scripts.destroyBubble import DestroyBubble
from shmup.scripts.destroyFish import DestroyFish
from shmup.scripts.fishMove import FishMove


class BubbleFactory():

    FINAL_SIZE = 48

    def __init__(self, gfxBubbleList, entBubbleList):
        self._gfxBubbleList = gfxBubbleList
        self._entBubbleList = entBubbleList

        fs = BubbleFactory.FINAL_SIZE
        BUBBLE01  = {
            "path": "resources/images/items/bubble.png",
            "textureName":"bubble01",
            "size": (128, 128),
            "finalSize":(fs,fs),
            "nbSprites": (1, 1),
        }
        BUBBLE02  = {
            "path": "resources/images/items/bubble.png",
            "textureName":"bubble02",
            "size": (128, 128),
            "finalSize":(int(fs/1.5),int(fs/1.5)),
            "nbSprites": (1, 1),
        }
        BUBBLE03  = {
            "path": "resources/images/items/bubble.png",
            "textureName":"bubble03",
            "size": (128, 128),
            "finalSize":(fs//2,fs//2),
            "nbSprites": (1, 1),
        }
        BUBBLE04  = {
            "path": "resources/images/items/bubble.png",
            "textureName":"bubble04",
            "size": (128, 128),
            "finalSize":(int(fs/2.5),int(fs/2.5)),
            "nbSprites": (1, 1),
        }
        self._bubbles = [
            BUBBLE01,
            BUBBLE02,
            BUBBLE03,
            BUBBLE04,
        ]

    def create(self, initPos):

        # Create entity
        eBubble = Entity("Bubble")

        # Select random shape
        idx    = randint(0,len(self._bubbles)-1)
        bubble = self._bubbles[idx]
        nbX   = bubble["nbSprites"][0]
        nbY   = bubble["nbSprites"][1]
        W     = bubble["size"][0] // nbX
        H     = bubble["size"][1] // nbY
        fSize = bubble["finalSize"]
        params = {
            "filePath": bubble["path"],
            "textureName": bubble["textureName"],
            "spriteBox": (nbX,nbY,W,H),
            "startIndex": 0,
            "endIndex": (W*H)-1,
            "frameDuration": 1 / 10,
            "size": fSize,
            "position":initPos
        }
        bubbleGfx     = GfxAnimatedSprite(params, ZIDX_BUBBLES, "bubbleGfx")
        params = {
            "mass"         : 0.01,
            "radius"       : fSize[0]/2,
            "mode"         : pymunk.Body.DYNAMIC,
            "pos"          : initPos,
            "sensor"       : False,
            "collisionType": COLL_TYPE_BUBBLE,
        }
        bubblePhy = PhysicDisc(params,"bubblePhy")
        gfxPhyLink = GfxPhyLink(bubbleGfx, bubblePhy, (0,0), "gfxphylink")

        bubbleMove    = BubbleMove(bubblePhy, "bubbleMove")
        bubbleDestroy = DestroyBubble(eBubble, bubbleGfx, self._gfxBubbleList, self._entBubbleList)

        # add all components to entity
        eBubble.addComponent(bubbleGfx)
        eBubble.addComponent(bubbleMove)
        eBubble.addComponent(bubbleDestroy)
        eBubble.addComponent(bubblePhy)
        eBubble.addComponent(gfxPhyLink)

        # return result
        return eBubble

