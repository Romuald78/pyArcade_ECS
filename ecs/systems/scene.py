## ============================================================
## IMPORTS
## ============================================================
import arcade
from common import constants



## ============================================================
## SCENE MANAGER (driven by the main class)
## ============================================================
class SceneSystem():

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self):
        # Scene names used in the main process
        self.currentSceneName = None
        self.nextSceneName    = None
        # Pause mode
        self.onPause          = False
        # Dict of userScenes
        self.scenes           = {}
        # Time and color used in the transition process
        self.currentTime      = 1
        self.maxTime          = 1
        self.color            = (0,0,0)


    ## -------------------------------------
    ## Scene list management
    ## -------------------------------------
    def addScene(self, sceneName, sceneRef):
        if sceneName not in self.scenes:
            self.scenes[sceneName] = sceneRef
            # select this scene if this is the first to be added
            if len(self.scenes) == 1:
                self.currentSceneName = sceneName
                self.currentTime      = 0
                self.maxTime          = sceneRef.getTransitionTimeIN()
                self.color            = sceneRef.getTransitionColorIN()
        else:
            raise ValueError(f"[ERR] cannot add scene '{sceneName}' : already in the list !")

    def remove(self, sceneName):
        if sceneName in self.scenes:
            # delete scene if not selected
            if self.currentSceneName != sceneName:
                del self.scenes[sceneName]
            else:
                raise ValueError(f"[ERR] cannot remove scene '{sceneName}' : currently selected !")
        else:
            raise ValueError(f"[ERR] cannot remove scene '{sceneName}' : not in the list !")


    ## -------------------------------------
    ## Scene control
    ## -------------------------------------
    def selectNewScene(self,sceneName):
        # Set the next scene if not currently in transition
        if self.nextSceneName != None:
            self.nextSceneName = sceneName
            self.maxTime       = self.scenes[self.currentSceneName].getTransitionTimeOUT()
            self.currentTime   = 0
            self.color         = self.scenes[self.currentSceneName].getTransitionColorOUT()
        else:
            raise ValueError(f"[ERR] cannot select scene {sceneName} : transition in progress !")

    def getCurrentSceneName(self):
        return self.currentSceneName

    def pause(self):
        self.onPause = True

    def resume(self):
        self.onPause = False

    def isPaused(self):
        return self.onPause


    ## -------------------------------------
    ## Transitions methods
    ## -------------------------------------
    def __updateTransition(self, deltaTime):
        # increase timer
        self.currentTime = self.currentTime + deltaTime
        # OUT phase
        if self.nextSceneName != None:
            if self.currentTime >= self.maxTime:
                # switch to IN phase
                self.currentSceneName = self.nextSceneName
                self.currentTime     -= self.maxTime
                self.maxTime          = self.scenes[self.nextSceneName].getTransitionTimeIN()
                self.color            = self.scenes[self.nextSceneName].getTransitionColorIN()
                self.nextSceneName    = None
        # IN Phase
        if self.nextSceneName == None:
            # saturate the current time
            self.currentTime = min(self.maxTime, self.currentTime)

    def __getTransitionColor(self):
        # OUT phase
        if self.nextSceneName != None:
            alpha = self.currentTime/self.maxTime
        # IN phase
        else:
            alpha = 1.0 - (self.currentTime/self.maxTime)
            if alpha <= 0:
                # no use to display a full transparent screen
                # when the transition is over
                return None
        # concatenate RGB and ALPHA
        alpha = int(255*alpha)
        return self.color + (alpha,)


    ## -------------------------------------
    ## Scene process
    ## -------------------------------------
    def updateCurrentScene(self, deltaTime):
        # we need at least one scene
        if self.currentSceneName != None:
            # update transition information
            self.__updateTransition(deltaTime)
            # check if we are not in pause mode
            if not self.onPause:
                # update
                self.scenes[self.currentSceneName].update(deltaTime)

    def drawCurrentScene(self):
        # we need at least one scene
        if self.currentSceneName != None:
            # draw current scene
            self.scenes[self.currentSceneName].draw()
            # draw color mask in case of transitions
            clr = self.__getTransitionColor()
            if clr != None:
               arcade.draw_rectangle_filled(constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT//2,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT,clr)


    ## -------------------------------------
    ## Input management
    ## -------------------------------------
    def dispatchKeyEvent(self, key, isPressed):
        if self.currentSceneName != None:
            self.scenes[self.currentSceneName].onKeyEvent(key, isPressed)

    def dispatchMouseButtonEvent(self, buttonName, x, y, isPressed):
        if self.currentSceneName != None:
            self.scenes[self.currentSceneName].onMouseButtonEvent(buttonName, x, y, isPressed)

    def dispatchMouseMotionEvent(self, x, y, dx, dy):
        if self.currentSceneName != None:
            self.scenes[self.currentSceneName].onMouseMotionEvent(x, y, dx, dy)

    def dispatchGamepadButtonEvent(self, gamepadNum, buttonName, isPressed):
        if self.currentSceneName != None:
            self.scenes[self.currentSceneName].onGamepadButtonEvent(gamepadNum, buttonName, isPressed)

    def dispatchGamepadAxisEvent(self, gamepadNum, axisName, analogValue):
        if self.currentSceneName != None:
            self.scenes[self.currentSceneName].onGamepadAxisEvent(gamepadNum, axisName, analogValue)

