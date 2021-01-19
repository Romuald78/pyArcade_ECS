### ====================================================================================================
### IMPORTS
### ====================================================================================================
from ecs.systems.sceneSystem import SceneSystem
from shmup.scenes.inGame import *


class Main:

    ### ====================================================================================================
    ### CONSTRUCTOR
    ### ====================================================================================================
    def __init__(self):
        self.sceneMgr = SceneSystem()
        self.sceneMgr.addScene( "InGame", InGame() )


    ### ====================================================================================================
    ### INIT
    ### ====================================================================================================
    def setup(self):
        pass


    ### ====================================================================================================
    ### UPDATE
    ### ====================================================================================================
    def update(self,deltaTime):
        self.sceneMgr.updateCurrentScene(deltaTime)
        

    ### ====================================================================================================
    ### RENDERING
    ### ====================================================================================================
    def draw(self):
        self.sceneMgr.drawCurrentScene()


    ### ====================================================================================================
    ### KEYBOARD EVENTS
    ### key is taken from : arcade.key.xxx
    ### ====================================================================================================
    def mainKeyEvent(self, key, isPressed):
        #print(f"key={key} - isPressed={isPressed}")
        self.sceneMgr.dispatchKeyEvent(key, isPressed)


    ### ====================================================================================================
    ### GAMEPAD BUTTON EVENTS
    ### buttonName can be "A", "B", "X", "Y", "LB", "RB", "VIEW", "MENU", "LSTICK", "RSTICK"
    ### ====================================================================================================
    def mainButtonEvent(self, gamepadNum,buttonName,isPressed):
        #print(f"GamePad={gamepadNum} - ButtonNum={buttonName} - isPressed={isPressed}")
        self.sceneMgr.dispatchGamepadButtonEvent(gamepadNum, buttonName, isPressed)


    ### ====================================================================================================
    ### GAMEPAD AXIS EVENTS
    ### axisName can be "X", "Y", "RX", "RY", "Z"
    ### ====================================================================================================
    def mainAxisEvent(self, gamepadNum,axisName,analogValue):
        #print(f"GamePad={gamepadNum} - AxisName={axisName} - Value={analogValue}")
        self.sceneMgr.dispatchGamepadAxisEvent(gamepadNum, axisName, analogValue)


    ### ====================================================================================================
    ### MOUSE MOTION EVENTS
    ### ====================================================================================================
    def mainMouseMotionEvent(self,x,y,dx,dy):
        #print(f"MOUSE MOTION : x={x}/y={y} dx={dx}/dy={dy}")
        self.sceneMgr.dispatchMouseMotionEvent(x, y, dx, dy)


    ### ====================================================================================================
    ### MOUSE BUTTON EVENTS
    ### mouse name can be "MOUSE_1", "MOUSE_2", ...
    ### ====================================================================================================
    def mainMouseButtonEvent(self,buttonName,x,y,isPressed):
        #print(f"MOUSE BUTTON : x={x}/y={y} buttonNum={buttonName} isPressed={isPressed}")
        self.sceneMgr.dispatchMouseButtonEvent(buttonName, x, y, isPressed)

