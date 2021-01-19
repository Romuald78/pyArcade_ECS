from ecs.components.gfx import *
from ecs.components.input import *
from ecs.components.script import *
from ecs.main.entity import *
from ecs.main.scene import *
from shmup.factories.GrassFactory import GrassFactory
from shmup.scripts.GrassMovement import GrassMovement
from shmup.scripts.scripts import MoveAnalog, Disappear


class InGame(Scene, Script):

    def __init__(self):
        super().__init__()

        NB_GRASS_ROWS = 4

        # --------------------------------------
        # Create Ninja
        # --------------------------------------
        # instanciate entity
        ninja = Entity()

        # Add button (gamepad)
        button = GamepadButton("hideButton", Input.ALL_GAMEPADS_ID, "A")
        ninja.addComponent("padButtA", button)
        # Add disappear script
        disappear = Disappear(button)
        ninja.addComponent("disappear", disappear)

        # Add ninja animated sprite
        params = {
            "filePath": f"images/ninja.png",
            "spriteBox": (7, 1, 120, 120),
            "startIndex": 1,
            "endIndex": 6,
            "frameDuration": 1 / 5,
            "size": (150, 150),
            "position": (750, (150 // 2) - 8),
            "flipH": False
        }
        zIndexNinja = 100 * (NB_GRASS_ROWS // 2) - 50 - 10
        ninjaRunR = GfxAnimatedSprite(self, params, zIndexNinja)
        params["flipH"] = True
        ninjaRunL = GfxAnimatedSprite(self, params, zIndexNinja)

        ninja.addComponent("runAnimL", ninjaRunL)
        ninja.addComponent("runAnimR", ninjaRunR)

        params = {
            "filePath": f"images/ninja.png",
            "spriteBox": (7, 1, 120, 120),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1,
            "size": (150, 150),
            "position": (750, (150 // 2) - 8),
            "flipH": False
        }
        ninjaIdleR = GfxAnimatedSprite(self, params, zIndexNinja)
        params["flipH"] = True
        ninjaIdleL = GfxAnimatedSprite(self, params, zIndexNinja)

        ninja.addComponent("idleL", ninjaIdleL)
        ninja.addComponent("idleR", ninjaIdleR)

        # Add X axis
        xAxis = GamepadAxis("xAxis", 0, "X")
        ninja.addComponent("inputAnalogX", xAxis)

        # Add move script
        script1 = MoveAnalog(ninjaRunR , xAxis, 10, disappear, True, False)
        script2 = MoveAnalog(ninjaIdleR, xAxis, 10, disappear, False, False)
        script3 = MoveAnalog(ninjaRunL , xAxis, 10, disappear, True, True)
        script4 = MoveAnalog(ninjaIdleL, xAxis, 10, disappear, False, True)
        ninja.addComponent("moveNinja1", script1)
        ninja.addComponent("moveNinja2", script2)
        ninja.addComponent("moveNinja3", script3)
        ninja.addComponent("moveNinja4", script4)

        # ADD NINJA entity to the world !
        self.addEntity("Ninja", ninja)


        # prepare character entity list
        charList = [ninja]

        # --------------------------------------
        # Create grass and interactions with characters
        # --------------------------------------
        # Instanciate entity for game mechanics
        gameMechanics = Entity()

        # Instanciate factory
        grassFact = GrassFactory(self)
        # Generate N grass-row-entities from factory
        for i in range(NB_GRASS_ROWS):
            ratio = 0.99-0.01*i/NB_GRASS_ROWS
            grass     = grassFact.create(self, 100, 0, 1500, 100*(i+1), 16+(40*i//NB_GRASS_ROWS),  84+(210*i//NB_GRASS_ROWS), (0, 255-(150*i//NB_GRASS_ROWS), 0, 245-(100*i//NB_GRASS_ROWS)))
            if i >= 0:
                grassMove = GrassMovement(charList, grass, ratio)
                gameMechanics.addComponent("grassMove"+str(i), grassMove)
            # ADD GRASS entity to the world !
            self.addEntity("Grass"+str(i), grass)

        # ADD MECHANICS entity to the world
        self.addEntity("gameMech", gameMechanics)





def tmpCode():
    # --------------------------------------
    # Create Panda
    # --------------------------------------
    # instanciate entity
    panda = Entity()
    # Add panda fixed sprite
    params = {
        "filePath": f"images/panda.png",
        "size": (125 // 2, 239 // 2),
        "position": (1000, (239 // 4)),
        "filterColor": (32, 255, 32)
    }
    zIndexPanda = 100 * (NB_GRASS_ROWS // 2) - 50
    pandaGfx = GfxSimpleSprite(self, params, zIndexPanda)
    panda.addComponent("character", pandaGfx)
    # Add X axis
    xAxis = GamepadAxis("xAxis", Input.ALL_GAMEPADS_ID, "X")
    panda.addComponent("inputAnalogX", xAxis)
    # Add move script
    scrMov = MoveAnalog(pandaGfx, xAxis, 15)
    panda.addComponent("movePanda", scrMov)

    # ADD PANDA entity to the world !
    self.addEntity("Panda", panda)

    pass