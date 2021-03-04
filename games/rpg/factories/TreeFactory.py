import arcade
import pymunk

from ecs.core.components.gfx import GfxAnimatedSprite
from ecs.core.components.input import Keyboard
from ecs.core.components.physic import PhysicDisc, PhysicBox
from ecs.core.components.transform import Transform
from ecs.core.main.entity import Entity
from ecs.user.script.follow import GfxFollowTransform
from games.rpg.constants import *
from games.rpg.scripts.move4dirs import Move4Dirs


class TreeFactory():

    def __init__(self):
        pass

    def create(self, initPos):

        treeSize = 128

        # Create Gfx components for animations
        # Prepare structures for character move
        # This contains the states of moving keys (left, right, up, down)
        gfx = GfxAnimatedSprite(1, compName="treeGfx")

        # Add animation
        params = { "animName"     : "idle",
                   "filePath"     : "games/rpg/resources/images/trees/tree01.png",
                   "spriteBox"    : (1, 1, 128, 128),
                   "startIndex"   : 0,
                   "endIndex"     : 0,
                   "frameDuration": 1 / 10,
                   "flipH"        : False,
                   "flipV"        : False,
                   "counter"      : 0,
                   "backAndforth" : False,
                   "facingDirection": 0,
                   "position"     : initPos,

                }
        gfx.addAnimation(params)
        # Offset
        offset = (0,treeSize/3)
        # Real position
        realPos = (initPos[0]+offset[0], initPos[1]+offset[1])
        # Set position and ZIndex of the gfx
        gfx.setPosition( realPos )
        gfx.setZIndex(ZIDX_GROUND+initPos[1])

        # Physic
        params = {
            "mass"         : 0.01,
            "size"         : (treeSize/2.2,treeSize/2),
            "mode"         : pymunk.Body.STATIC,
            "pos"          : initPos,
            "sensor"       : False,
            "collisionType": COLL_TREES,
        }
        phy = PhysicBox(params)
        params = {
            "mass"         : 0.01,
            "radius"       : treeSize/4,
            "mode"         : pymunk.Body.STATIC,
            "pos"          : (initPos[0]-treeSize/4.4,initPos[1]),
            "sensor"       : False,
            "collisionType": COLL_TREES,
        }
        phy2 = PhysicDisc(params)
        params["pos"] = (initPos[0]+treeSize/4.4,initPos[1])
        phy3 = PhysicDisc(params)

        # Create entity ad add components to it
        entity = Entity("tree")
        entity.addComponent(gfx)
        entity.addComponent(phy)
        entity.addComponent(phy2)
        entity.addComponent(phy3)

        # Return entity
        return entity


