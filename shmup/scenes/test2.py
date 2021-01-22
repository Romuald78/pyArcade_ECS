import arcade

from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite, GfxSimpleEmitter
from ecs.core.components.input import Keyboard, GamepadAxis, Input
from ecs.user.script.gfxpos import LimitBox, Follow, LimitCircle
from shmup.common.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ecs.user.idle.counters import UserCounter
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.scripts.test2_scripts import ModifLife, MoveGfx, MoveStick, PauseScene, ShowHidePanda


class SceneTest2(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        self.setDebugMode(False, True)

        # Create Entity
        entity = Entity("TestEntity")

        #===== NINJA Gfx Animated Sprite Component =====
        params = {
            "filePath": f"images/ninja.png",
            "spriteBox": (7, 1, 120, 120),
            "startIndex": 1,
            "endIndex": 6,
            "frameDuration": 1 / 24,
            "size": (150, 150)
        }
        ninjaGfx  = GfxAnimatedSprite(self, params, 10, "Ninja")

        #===== PANDA Gfx Simple sprite Component =====
        params = {
            "filePath": f"images/panda.png",
            "size": (125 // 2, 239 // 2)
        }
        pandaGfx  = GfxSimpleSprite(self, params, 20, "Panda")

        #===== PANDA Gfx Emitter Component =====
        params = {  "x0"          : 1000,
                    "y0"          : 500,
                    "partNB"      : 100,
                    "partSize"    : 239,
                    "partScale"   : 0.25,
                    "partSpeed"   : 5.0,
                    "maxLifeTime" : 1.0,
                    "color"       : (255,255,0),
                    "startAlpha"  : 100,
                    "endAlpha"    : 0,
                    "spriteBox"   : (1,1,125,239),
                    "spriteSelect": (0,0),
                    "imagePath"   : "images/panda.png"
        }
        emitterGfx = GfxSimpleEmitter(self, params, 30, "SimpleEmitter")

        #===== PANDA Gfx Simple sprite Component =====
        params = {
            "filePath": f"images/grass.png",
            "size": (200, 200)
        }
        grassGfx  = GfxSimpleSprite(self, params, 40, "Grass")


        #===== Input Components =====
        keyUp     = Keyboard("IncreaseLife", arcade.key.UP  , "KeyUP"  )
        keyDown   = Keyboard("DecreaseLife", arcade.key.DOWN, "KeyDOWN")
        keyP      = Keyboard("SelectScene", arcade.key.P, "KeyP")
        keyX      = Keyboard("scrShowHide", arcade.key.X, "KeyX")
        keyAdd    = Keyboard("FrontLayer", arcade.key.NUM_ADD, "KeyAdd")
        keySub    = Keyboard("RearLayer", arcade.key.NUM_SUBTRACT, "KeySub")
        axisX     = GamepadAxis("movePandaX", Input.ALL_GAMEPADS_ID,"X",0.2,"AxisX")
        axisY     = GamepadAxis("movePandaY", Input.ALL_GAMEPADS_ID,"Y",0.2,"AxisY")

        #===== Idle Components =====
        life      = UserCounter(0,11,5, True, "Life")

        #===== Script Components =====
        modifLife   = ModifLife(keyUp, keyDown, life, "ModifLife")
        moveGfx     = MoveGfx(ninjaGfx, life, "MoveGfx")
        moveStick   = MoveStick(pandaGfx, axisX, axisY, "MoveStick")
        pause       = PauseScene(self, keyP, "PauseGame")
        showHide    = ShowHidePanda(keyAdd, keySub, keyX, pandaGfx)
        limitPos    = LimitBox(pandaGfx, (1000, 1080),(1920, 350), "LimitPandaBox")
        limitCircle = LimitCircle(pandaGfx, (1075, 500), 200, "LimitPandaCircle")
        follow      = Follow(pandaGfx, grassGfx, "FollowPanda")

        # Configure some components to be still active in the scene when paused
        keyP.enableOnPause()
        pause.enableOnPause()



        # ECS Gfx Components
        entity.addComponent(ninjaGfx)
        entity.addComponent(pandaGfx)
        entity.addComponent(emitterGfx)
        entity.addComponent(grassGfx)
        # ECS Input Components
        entity.addComponent(keyUp)
        entity.addComponent(keyDown)
        entity.addComponent(keyP)
        entity.addComponent(keyX)
        entity.addComponent(keyAdd)
        entity.addComponent(keySub)
        entity.addComponent(axisX)
        entity.addComponent(axisY)
        # ECS Idle Components
        entity.addComponent(life)
        # ECS Script Components
        entity.addComponent(modifLife)
        entity.addComponent(moveGfx)
        entity.addComponent(moveStick)
        entity.addComponent(pause)
        entity.addComponent(showHide)
        entity.addComponent(limitPos)
        entity.addComponent(limitCircle)
        entity.addComponent(follow)

        # Add entity to scene
        self.addEntity(entity)

