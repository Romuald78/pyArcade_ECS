import arcade
import pymunk

from ecs.core.components.gfx import GfxAnimatedSprite
from ecs.core.components.input import Keyboard
from ecs.core.components.physic import PhysicDisc
from ecs.core.components.transform import Transform
from ecs.core.main.entity import Entity
from ecs.user.script.follow import GfxFollowTransform, TransformFollowPhysic
from games.rpg.constants import *
from games.rpg.scripts.move4dirs import Move4Dirs


class PlayerFactory():

    def __init__(self):
        pass

    def create(self):

        playerSize = 64

        # Create Gfx components for animations
        # Prepare structures for character move
        # This contains the states of moving keys (left, right, up, down)
        gfx = GfxAnimatedSprite(NB_DIRECTIONS)

        # Add animations for the 8 direction character
        index = [6, 3, 9, 0]
        for i in range(NB_DIRECTIONS):
            # Add walking animations for each facing_direction
            params = { "animName"       : "walk",
                       "filePath"       : "games/rpg/resources/images/characters/Male/Male 01-1.png",
                       "spriteBox"      : (3, 4, 32, 32),
                       "startIndex"     : index[i],
                       "endIndex"       : index[i] + 2,
                       "frameDuration"  : 1 / 10,
                       "flipH"          : False,
                       "flipV"          : False,
                       "counter"        : 0,
                       "backAndForth"   : True,
                       "facingDirection": i
                    }
            gfx.addAnimation(params)

            # Add idle animations for each facing_direction
            params["animName"]   = "idle"
            params["startIndex"] = index[i] + 1
            params["endIndex"]   = index[i] + 1
            gfx.addAnimation(params)

        gfx.setPosition( (SCREEN_WIDTH//2, SCREEN_HEIGHT//2) )
        gfx.setScale(playerSize/32.0)

        # Add keyboard management
        keyL = Keyboard("moveLeft" , arcade.key.LEFT , "keyLEFT" )
        keyR = Keyboard("moveRight", arcade.key.RIGHT, "keyRIGHT")
        keyU = Keyboard("moveUp"   , arcade.key.UP   , "keyUP"   )
        keyD = Keyboard("moveDown" , arcade.key.DOWN , "keyDOWN" )

        # transform
        trans = Transform("transform")
        trans.position = (960, 540, ZIDX_GROUND)

        # Physic
        params = {
            "mass"         : 0.001,
            "radius"       : playerSize*0.33,
            "mode"         : pymunk.Body.DYNAMIC,
            "pos"          : (960,540),
            "elasticity"   : 0.0,
            "friction"     : 1.0,
            "sensor"       : False,
            "collisionType": COLL_PLAYERS,
        }
        phy = PhysicDisc(params, "phy")

        # Script to move the character with keyboard keys
        moveChar = Move4Dirs( gfx, phy, keyL, keyR, keyU, keyD, 300)
        follow1  = TransformFollowPhysic(trans, phy)
        follow2  = GfxFollowTransform(gfx, trans, offsetXY=(0,playerSize/2.5), topDownZ=True)

        # Create entity ad add components to it
        entity = Entity("player")
        entity.addComponent(gfx)
        entity.addComponent(trans)
        entity.addComponent(phy)
        entity.addComponent(keyL)
        entity.addComponent(keyR)
        entity.addComponent(keyU)
        entity.addComponent(keyD)
        entity.addComponent(moveChar)
        entity.addComponent(follow1)
        entity.addComponent(follow2)

        # Return entity
        return entity


