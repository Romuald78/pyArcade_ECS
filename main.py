### ====================================================================================================
### IMPORTS
### ====================================================================================================
from ecs.core.systems.sceneSystem import SceneSystem
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

