### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade
from arcade.experimental.lights import LightLayer, Light

from ecs.core.systems.sceneSystem import SceneSystem
from shmup.common.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from shmup.scenes.endgamescene import EndGameScene
from shmup.scenes.intro import DisplayGGJ, DisplayRPH, DisplayArcade
from shmup.scenes.loading import Loading
from shmup.scenes.selection import Selection
from shmup.scenes.splash import SplashScreen
from shmup.scenes.underwater import UnderWater


class Main:



    ### ====================================================================================================
    ### CONSTRUCTOR
    ### ====================================================================================================
    def __init__(self):
        self._sceneMgr = SceneSystem()

        # GAME scenes
        self._sceneMgr.addScene(Loading      (self._sceneMgr, "LOAD")     )
        self._sceneMgr.addScene(DisplayGGJ   (self._sceneMgr, "GGJ")      )
        self._sceneMgr.addScene(DisplayArcade(self._sceneMgr, "ARCADE")   )
        self._sceneMgr.addScene(DisplayRPH   (self._sceneMgr, "RPH")      )
        self._sceneMgr.addScene(SplashScreen (self._sceneMgr, "SPLASH")   )
        self._sceneMgr.addScene(Selection    (self._sceneMgr, "SELECTION"))
        self._sceneMgr.addScene(UnderWater   (self._sceneMgr, "UNDERWATER"))
        self._sceneMgr.addScene(EndGameScene (self._sceneMgr, "ENDGAME"))


        self._lightLayer2 = LightLayer(SCREEN_WIDTH,SCREEN_HEIGHT)
        self._lightLayer3 = LightLayer(SCREEN_WIDTH,SCREEN_HEIGHT)
        light2 = Light(500,500,250,(0,255,0),'soft')
        light3 = Light(750, 250, 250, (255, 0, 0), 'soft')
        self._lightLayer2.add(light2)
        self._lightLayer3.add(light3)


    ### ====================================================================================================
    ### INIT
    ### ====================================================================================================
    def setup(self):
        pass


    ### ====================================================================================================
    ### UPDATE
    ### ====================================================================================================
    def update(self,deltaTime):
        self._sceneMgr.updateCurrentScene(deltaTime)
        

    ### ====================================================================================================
    ### RENDERING
    ### ====================================================================================================
    def draw(self):
        self._sceneMgr.drawCurrentScene()

#        arcade.draw_rectangle_filled(750, 500, 1000, 1000, (128, 128, 255))
#        with self._lightLayer2:
#            arcade.draw_rectangle_filled(250,250,500,500,(128,128,128))
#        self._lightLayer2.draw(ambient_color=(255,255,255))
#        with self._lightLayer3:
#            arcade.draw_rectangle_filled(750,250,500,500,(128,128,128))
#        self._lightLayer3.draw(ambient_color=(255,255,255))


    ### ====================================================================================================
    ### KEYBOARD EVENTS
    ### key is taken from : arcade.key.xxx
    ### ====================================================================================================
    def mainKeyEvent(self, key, isPressed):
        #print(f"key={key} - isPressed={isPressed}")
        self._sceneMgr.dispatchKeyEvent(key, isPressed)


    ### ====================================================================================================
    ### GAMEPAD BUTTON EVENTS
    ### buttonName can be "A", "B", "X", "Y", "LB", "RB", "VIEW", "MENU", "LSTICK", "RSTICK"
    ### ====================================================================================================
    def mainButtonEvent(self, gamepadNum,buttonName,isPressed):
        #print(f"GamePad={gamepadNum} - ButtonNum={buttonName} - isPressed={isPressed}")
        self._sceneMgr.dispatchGamepadButtonEvent(gamepadNum, buttonName, isPressed)


    ### ====================================================================================================
    ### GAMEPAD AXIS EVENTS
    ### axisName can be "X", "Y", "RX", "RY", "Z"
    ### ====================================================================================================
    def mainAxisEvent(self, gamepadNum,axisName,analogValue):
        #print(f"GamePad={gamepadNum} - AxisName={axisName} - Value={analogValue}")
        self._sceneMgr.dispatchGamepadAxisEvent(gamepadNum, axisName, analogValue)


    ### ====================================================================================================
    ### MOUSE MOTION EVENTS
    ### ====================================================================================================
    def mainMouseMotionEvent(self,x,y,dx,dy):
        #print(f"MOUSE MOTION : x={x}/y={y} dx={dx}/dy={dy}")
        self._sceneMgr.dispatchMouseMotionEvent(x, y, dx, dy)


    ### ====================================================================================================
    ### MOUSE BUTTON EVENTS
    ### mouse name can be "MOUSE_1", "MOUSE_2", ...
    ### ====================================================================================================
    def mainMouseButtonEvent(self,buttonName,x,y,isPressed):
        #print(f"MOUSE BUTTON : x={x}/y={y} buttonNum={buttonName} isPressed={isPressed}")
        self._sceneMgr.dispatchMouseButtonEvent(buttonName, x, y, isPressed)

