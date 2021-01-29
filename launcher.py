### ====================================================================================================
### IMPORTS
### ====================================================================================================
import arcade

from shmup.common import constants
from main import Main
import os
import time


### ====================================================================================================
### CONSTANTS
### ====================================================================================================
TITLE = "pyArcade-ECS"



### ====================================================================================================
### GAME CLASS
### ====================================================================================================
class Launcher(arcade.Window):

    #FEATURE : how to create and add a scene outside the Main class ???

    # FEATURE : try to remove all arcade dependencies in the Main class (keep arcade in launcher)

    # FEATURE : REVIEW the design in order to remove as much as possible user scene calls to
    # ECS system May be the Main file could be a upper class for the real user main ... to be continued

    BUTTON_NAMES = ["A",
                    "B",
                    "X",
                    "Y",
                    "LB",
                    "RB",
                    "VIEW",
                    "MENU",
                    "LSTICK",
                    "RSTICK",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    ]

    AXIS_NAMES =["X",
                 "Y",
                 "RX",
                 "RY",
                 "Z",
                ]


    # ----------------------------------
    # PRIVATE METHODS FOR INPUT MANAGEMENT
    # ----------------------------------
    def __onButtonPressed(self, _gamepad, button):
        idx = self.gamepads[_gamepad]
        if Launcher.BUTTON_NAMES[button] != None:
            self.onButtonPressed(idx, Launcher.BUTTON_NAMES[button])
    def __onButtonReleased(self, _gamepad, button):
        idx = self.gamepads[_gamepad]
        if Launcher.BUTTON_NAMES[button] != None:
            self.onButtonReleased(idx, Launcher.BUTTON_NAMES[button])
    def __onCrossMove(self, _gamepad, x, y):
        idx = self.gamepads[_gamepad]
        self.onCrossMove(idx, x, -y)
    def __onAxisMove(self, _gamepad, axis, value):
        idx = self.gamepads[_gamepad]
        self.onAxisMove(idx, axis, value)



    # ----------------------------------
    # CONSTRUCTOR
    # ----------------------------------
    def __init__(self, width, height, title, fullScreen):
        # Init application window
        super().__init__(width, height, title, fullScreen)

        # BUG : fit application size to screen resolution
        # Resize and center application windows in order
        # to fit with the current screen resolution
        # arcade.set_background_color(arcade.color.AMAZON)
        # self.set_fullscreen(True)
        # self.set_viewport(0, 1920*2, 0, 1080*2)

        # FEATURE : use key and mouse modifiers (Ctrl, Alt, Shift, ...)

        # Init process object
        self.process = Main()
        # Set application window background color
        arcade.set_background_color(arcade.color.BLACK)
        # Store gamepad list
        self.gamepads = arcade.get_game_controllers()
        # Check every connected gamepad
        if self.gamepads:
            for g in self.gamepads:
                # Link all gamepad callbacks to the current class methods
                g.open()
                g.on_joybutton_press   = self.__onButtonPressed
                g.on_joybutton_release = self.__onButtonReleased
                g.on_joyhat_motion     = self.__onCrossMove
                g.on_joyaxis_motion    = self.__onAxisMove
            # Transform list into a dictionary to get its index faster
            self.gamepads = { self.gamepads[idx]:idx for idx in range(len(self.gamepads)) }
        else:
            print("There are no Gamepad connected !")
            self.gamepads = None
        # FPS counter
        self.updateTime  = []
        self.drawTime    = []
        self.frameTime   = []


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                                SETUP your game here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def setup(self):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.setup()
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                               DRAW your game elements here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_draw(self):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        measure = time.time()
        arcade.start_render()
        self.process.draw()
        measure = time.time() - measure

        self.drawTime.append(measure)
        self.drawTime = self.drawTime[-60:]
        #arcade.draw_text("FPS   : "+str(int(60 / sum(self.frameTime))), 12, 12, (255, 255, 255))
        #arcade.draw_text("Draw  : "+str(round(sum(self.updateTime)*50/3,3))+"ms"      , 12, 24, (255, 255, 255))
        #arcade.draw_text("Update: "+str(round(sum(self.drawTime  )*50/3,3))+"ms"      , 12, 36, (255, 255, 255))
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #                                  UPDATE your game model here
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def update(self, delta_time):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        measure = time.time()
        self.process.update(delta_time)
        measure = time.time() - measure
        self.updateTime.append(measure)
        self.updateTime = self.updateTime[-60:]
        self.frameTime.append(delta_time)
        self.frameTime = self.frameTime[-60:]
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # KEY PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_key_press(self, key, modifiers):
        # Close application if ESCAPE key is hit
        if key == arcade.key.ESCAPE:
            self.close()
        # switch between full screen and window mode
        if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainKeyEvent(key, True)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # KEY RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_key_release(self, key, modifiers):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainKeyEvent(key, False)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD BUTTON PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onButtonPressed(self, gamepadNum, buttonName):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainButtonEvent(gamepadNum,buttonName,True)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD BUTTON RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onButtonReleased(self, gamepadNum, buttonName):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainButtonEvent(gamepadNum,buttonName,False)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD CROSSPAD events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onCrossMove(self, gamepadNum, xValue, yValue):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainAxisEvent(gamepadNum, "X", xValue)
        self.process.mainAxisEvent(gamepadNum, "Y", yValue)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # GAMEPAD AXIS events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def onAxisMove(self, gamepadNum, axisName, analogValue):
        # normalize the Z axis
        if axisName == "z":
            analogValue = -analogValue
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainAxisEvent(gamepadNum,axisName.upper(),analogValue)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # MOUSE MOTION events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_mouse_motion(self, x, y, dx, dy):
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainMouseMotionEvent(x,y,dx,dy)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # MOUSE BUTTON PRESSED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_mouse_press(self, x, y, button, modifiers):
        # normalize button name
        buttonName = "M" + str(button)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainMouseButtonEvent(buttonName,x,y,True)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # MOUSE BUTTON RELEASED events
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def on_mouse_release(self, x, y, button, modifiers):
        # Normalize the button name
        buttonName = "M" + str(button)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#
        self.process.mainMouseButtonEvent(buttonName,x,y,False)
        #- - - - - - - - - - - - - - - - - - - - - - - - -#



### ====================================================================================================
### MAIN PROCESS
### ====================================================================================================
def main():
    # add current file path
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)

    width      = constants.SCREEN_WIDTH
    height     = constants.SCREEN_HEIGHT
    title      = TITLE
    fullScreen = True

    game = Launcher(width, height, title, fullScreen)
    game.set_vsync(True)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()


