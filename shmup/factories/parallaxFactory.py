from ecs.core.main.entity import Entity
from ecs.user.script.parallax import Parallax
from shmup.common.constants import *


class ParallaxFactory():

    def __init__(self):
        pass

    def create(self, speed=1.5, bgOnly=False):

        eParallax = Entity()

        # Backgrounds
        for i in range(1,5):
            prlx = Parallax(eParallax,
                            f"resources/images/parallax/sea/bg0{i}.png",
                            (SCREEN_WIDTH,SCREEN_HEIGHT),
                            (SCREEN_WIDTH,SCREEN_HEIGHT),
                            ZIDX_BG-i,
                            (-i/10)*speed,
                            "prlxBG")
            eParallax.addComponent(prlx)

        if not bgOnly:

            # Plants back
            for i in range(1,3):
                prlx = Parallax(eParallax,
                                f"resources/images/parallax/sea/plant0{i}.png",
                                (SCREEN_WIDTH,SCREEN_HEIGHT),
                                (SCREEN_WIDTH,SCREEN_HEIGHT),
                                ZIDX_BG-i-4,
                                (-(i+4)/10)*speed,
                                "prlxPlants")
                eParallax.addComponent(prlx)


            # Sand
            sand = Parallax(eParallax,
                            f"resources/images/parallax/sea/sand.png",
                            (SCREEN_WIDTH,SCREEN_HEIGHT),
                            (SCREEN_WIDTH,SCREEN_HEIGHT),
                            ZIDX_BG-7,
                            (-7/10)*speed,
                            "prlxSand")
            eParallax.addComponent(sand)
            # Plant front
            plant = Parallax(eParallax,
                            f"resources/images/parallax/sea/plant03.png",
                            (SCREEN_WIDTH, SCREEN_HEIGHT),
                            (SCREEN_WIDTH, SCREEN_HEIGHT),
                             ZIDX_FG,
                            (-8 / 10) * speed,
                            "prlxPlant")
            eParallax.addComponent(plant)
            # Coral front
            coral = Parallax(eParallax,
                            f"resources/images/parallax/sea/coral.png",
                            (SCREEN_WIDTH, SCREEN_HEIGHT),
                            (SCREEN_WIDTH, SCREEN_HEIGHT),
                             ZIDX_FG-1,
                            (-9 / 10) * speed,
                            "prlxCoral")
            eParallax.addComponent(coral)
            # Rock front
            rock = Parallax(eParallax,
                            f"resources/images/parallax/sea/rocks.png",
                            (SCREEN_WIDTH, SCREEN_HEIGHT),
                            (SCREEN_WIDTH, SCREEN_HEIGHT),
                            ZIDX_FG-2,
                            (-10 / 10) * speed,
                            "prlxRock")
            eParallax.addComponent(rock)

        # Return entity
        return eParallax