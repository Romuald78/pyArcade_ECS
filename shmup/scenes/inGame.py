from ecs.components.gfx import *
from ecs.components.input import *
from ecs.components.script import *
from ecs.main.entity import *
from ecs.main.scene import *
from shmup.factories.GrassFactory import GrassFactory
from shmup.scripts.GrassMovement import GrassMovement
from shmup.scripts.scripts import ScrMoveKey


class InGame(Scene, Script):

    def __init__(self):
        super().__init__()


        # --------------------------------------
        # Create Panda
        # --------------------------------------
        N = 6

        panda = Entity()

        # Add panda fixed sprite
        params = {
            "filePath": f"images/panda.png",
            "size": (125 // 2, 239 // 2),
            "position": (1000, (239 // 4)),
            "filterColor": (32,255,32)
        }
        pandaGfx = GfxSimpleSprite(params,100*(N//2)-50)
        panda.addComponent("Panda", pandaGfx)

        # Add X axis
        xAxis = GamepadAxis("xAxis", Input.ALL_GAMEPADS_ID, "X")
        panda.addComponent("inputAnalogX", xAxis)

        # Add script
        script1 = ScrMoveKey(pandaGfx, xAxis, 16)
        panda.addComponent("moveWithKeys", script1)

        # ADD PANDA to the world !
        self.addEntity("Panda",    panda)

        # --------------------------------------
        # Create grass and interactions with panda
        # --------------------------------------
        gameMechanics = Entity()

        grassFact = GrassFactory(self)
        for i in range(N):
            ratio = 0.999-0.005*i
            grass     = grassFact.create(100, 0, 1500, 100*(i+1), 16+(8*i),  84+(42*i), (0, 255-(40*i), 0, 245-(10*i)))
            grassMove = GrassMovement(panda, grass, ratio)
            gameMechanics.addComponent("scrGrMvov"+str(i), grassMove)
            # ADD GRASS to the world !
            self.addEntity("Grass"+str(i), grass)

        # ADD MECHANICS to the world
        self.addEntity("gameMech", gameMechanics)


