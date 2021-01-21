import arcade

from ecs.components.gfx import GfxSimpleSprite, GfxAnimatedSprite
from ecs.components.input import Keyboard, GamepadAxis, Input
from shmup.common.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ecs.libRGR.user.counters import UserCounter
from ecs.main.entity import Entity
from ecs.main.scene import Scene
from shmup.scripts.test2_scripts import ModifLife, MoveGfx, MoveStick, PauseScene


class SceneTest2(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        self.setDebugMode(False, True)

        # Create Entity
        entity = Entity("TestEntity")

        # Create components
        params = {
            "filePath": f"images/ninja.png",
            "spriteBox": (7, 1, 120, 120),
            "startIndex": 1,
            "endIndex": 6,
            "frameDuration": 1 / 24,
            "size": (150, 150)
        }
        ninjaGfx  = GfxAnimatedSprite(self, params, 0, "Ninja")
        params = {
            "filePath": f"images/panda.png",
            "size": (125 // 2, 239 // 2)
        }
        pandaGfx  = GfxSimpleSprite(self, params, 10, "Panda")
        keyUp     = Keyboard("IncreaseLife", arcade.key.UP  , "KeyUP"  )
        keyDown   = Keyboard("DecreaseLife", arcade.key.DOWN, "KeyDOWN")
        keyP      = Keyboard("SelectScene", arcade.key.P, "KeyP")
        axisX     = GamepadAxis("movePandaX", Input.ALL_GAMEPADS_ID,"X",0.2,"AxisX")
        axisY     = GamepadAxis("movePandaY", Input.ALL_GAMEPADS_ID,"Y",0.2,"AxisY")
        life      = UserCounter(0,10,5, True, "Life")
        modifLife = ModifLife(keyUp, keyDown, life, "ModifLife")
        moveGfx   = MoveGfx(ninjaGfx, life, "MoveGfx")
        moveStick = MoveStick(pandaGfx, axisX, axisY, "MoveStick")
        pause     = PauseScene(self, keyP, "PauseGame")

        # Configure some components to be still active in the scene when paused
        keyP.enableOnPause()
        pause.enableOnPause()

        # add components to entity
        entity.addComponent(ninjaGfx)
        entity.addComponent(pandaGfx)
        entity.addComponent(keyUp)
        entity.addComponent(keyDown)
        entity.addComponent(keyP)
        entity.addComponent(axisX)
        entity.addComponent(axisY)
        entity.addComponent(life)
        entity.addComponent(modifLife)
        entity.addComponent(moveGfx)
        entity.addComponent(moveStick)
        entity.addComponent(pause)

        # Add entity to scene
        self.addEntity(entity)
