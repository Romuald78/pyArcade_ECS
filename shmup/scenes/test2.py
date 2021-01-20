import arcade

from shmup.common.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ecs.libRGR.user.counters import UserCounter
from ecs.main.entity import Entity
from ecs.main.scene import Scene


class InGame(Scene):

    def __init__(self):
        # Init parent
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setDebugMode(False, True)

        # Create Entity
        entity = Entity("TestEntity")

        # Create components
        life = UserCounter(0,1000,750, True, "LIFE")

        # add components to entity
        entity.addComponent(life)

        # Add entity to scene
        self.addEntity(entity)

    def drawDebugInfo(self):
        refX = 20
        refY = SCREEN_HEIGHT-20
        entities = self.getEntityList()
        for ent in entities:
            arcade.draw_text(ent.getName(), refX, refY, (255, 255, 255), 12)
            refY -= 15
            components = ent.getComponentList()
            for comp in components:
                arcade.draw_text(comp.getName(), refX+50, refY, (255, 255, 255), 12)
                refY -= 15