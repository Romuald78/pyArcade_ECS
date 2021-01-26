import pymunk

from ecs.core.components.gfx import GfxSimpleSprite
from ecs.core.components.input import GamepadButton, Input
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.common.constants import *
from shmup.scripts.transitions import SwitchToScene


class TestPyMunk(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)

        self._space = pymunk.Space()
        self._space.gravity = 0, -1000

        self._body = pymunk.Body(1,1666)
        self._body.position = 500,500
        self._shape = pymunk.Poly.create_box(self._body,(20,20))
        self._space.add(self._body, self._shape)
        self._info = pymunk.SpaceDebugDrawOptions()

        self._space.remove(self._body)
        self._space.remove(self._shape)

    def update(self, deltaTime):
        super().update(deltaTime)
        self._space.step(deltaTime)
        self._space.debug_draw(self._info)
