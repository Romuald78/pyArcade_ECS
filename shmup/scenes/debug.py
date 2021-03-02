import arcade

from ecs.core.components.input import Keyboard
from ecs.core.components.script import Script
from ecs.core.components.sfx import Music
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.common.constants import *


class DebugScene(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)

    def init(self, params):

        # Create music component
        params = {
            "musicPath": "resources/sfx/music/test001.mp3",
            "volume"   : 1.0,
            "pan"      : 0.0,
            "loop"     : True
        }
        music = Music(params)

        musicList = [music]

        # Create key components
        keySpace = Keyboard( "playpause", arcade.key.SPACE     )
        keyBack  = Keyboard( "back"     , arcade.key.BACKSPACE )
        keyS     = Keyboard( "stop"     , arcade.key.S         )
        keyLeft  = Keyboard( "RW"       , arcade.key.LEFT      )
        keyRight = Keyboard( "FF"       , arcade.key.RIGHT     )
        keyUp    = Keyboard( "VolUP"    , arcade.key.UP        )
        keyDown  = Keyboard( "VolDOWN"  , arcade.key.DOWN      )

        # Create script
        scrMusic = DebugMusicScript(musicList, keySpace, keyBack, keyS, keyLeft, keyRight, keyUp, keyDown)

        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(music   )
        entity.addComponent(keySpace)
        entity.addComponent(keyBack )
        entity.addComponent(keyS    )
        entity.addComponent(keyLeft )
        entity.addComponent(keyRight)
        entity.addComponent(keyUp   )
        entity.addComponent(keyDown )
        entity.addComponent(scrMusic)

        # Add entity to the scene
        self.addEntity(entity)



    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 0.1
    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 0.1


class DebugMusicScript(Script):

    def __init__(self, musicList, keySpace, keyBack, keyS, keyLeft, keyRight, keyUp, keyDown, compName="DbgScr"):
        super().__init__(compName)
        self._playPause  = keySpace
        self._rewind     = keyBack
        self._stop       = keyS
        self._musics     = musicList
        self._FF         = keyRight
        self._RW         = keyLeft
        self._volUp      = keyUp
        self._volDown    = keyDown
        self._musicIndex = 0

    def updateScript(self, scriptName, deltaTime):
        # current music
        music = self._musics[self._musicIndex]

        # PLAY / PAUSE
        if self._playPause.hasBeenPressed():
            if music.isPlaying():
                music.pause()
            else:
                music.play()

        # REWIND
        if self._rewind.hasBeenPressed():
            music.fullRewind()

        # STOP
        if self._stop.hasBeenPressed():
            music.stop()

        # Fast Forward and Fast Rewind
        if self._FF.isPressed():
            music.fastForward(0.1)
        if self._RW.isPressed():
            music.rewind(0.1)

        # Volume management
        if self._volUp.isPressed():
            music.increaseVolume(0.01)
        if self._volDown.isPressed():
            music.decreaseVolume(0.01)


