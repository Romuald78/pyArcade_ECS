
## ============================================================
## IMPORTS
## ============================================================
import utils
from ecs.core.components.component import Component



## ============================================================
## SFX COMPONENT
## ============================================================


class Music(Component):

    # --------------------------------------------
    # CONSTRUCTOR
    # --------------------------------------------
    def __init__(self, params, compName=None):
        if compName == None :
            compName = "MUSIC"
        super().__init__(compName)
        # Retrieve parameters
        musicPath = params["musicPath"]
        volume = 1.0 if not "volume" in params    else params["volume"]
        pan    = 0.0 if not "pan"    in params    else params["pan"]
        loop   = False if not "loop" in params else params["loop"]
        # store file info
        self._music    = utils.createSound(musicPath)
        self._volume   = volume
        self._loop     = loop
        self._pan      = pan
        self._lastTime = 0
        self._playing  = False
        # Create player by playing the track and stopping immediately
        self._player   = self._music.play(volume, pan, loop)
        self._player.pause()

    # method to get current type
    def getType(self):
        return Component.TYPE_MUSIC


    # --------------------------------------------
    # PLAY MANAGEMENT
    # --------------------------------------------
    def play(self):
        # Play current music from the last pause/stop time
        # using the current volume, span, loop
        self._player.seek(self._lastTime)
        self._player.play()
        self._playing = True

    def pause(self):
        self._player.pause()
        self._lastTime = self._player.time
        self._playing = False

    def fullRewind(self):
        self._lastTime = 0
        if self.isPlaying():
            self._player.seek(self._lastTime)

    def stop(self):
        self._lastTime = 0
        self._player.pause()
        self._playing = False

    def isFinished(self):
        return self._music.is_complete()

    def isPlaying(self):
        return self._playing


    # --------------------------------------------
    # GETTERS
    # --------------------------------------------
    def getVolume(self):
        return self._volume

    def getPan(self):
        return self._pan

    def isLooping(self):
        return self._loop

    def getDuration(self):
        return self._music.get_length()

    def getCurrentTime(self):
        return self._music.get_stream_position(self._player)

    def getPercent(self):
        return self.getCurrentTime()/self.getDuration()

    # --------------------------------------------
    # SETTERS
    # --------------------------------------------
    def setVolume(self, newVolume):
        self._volume = max(0.0, min(1.0, newVolume))
        self._music.set_volume(self._volume, self._player)

    def _updateVolume(self, deltaVol):
        self.setVolume( self._volume+deltaVol )

    def increaseVolume(self, deltaVol):
        if deltaVol > 0:
            self._updateVolume(deltaVol)

    def decreaseVolume(self, deltaVol):
        if deltaVol > 0:
            self._updateVolume(-deltaVol)

    def setTime(self, newTime):
        self._lastTime = newTime
        self._player.seek(newTime)

    def _updateTime(self, deltaTime):
        # Increase or decrease current time
        self._lastTime = max(0.0, self.getCurrentTime()+deltaTime)
        self._player.seek(self._lastTime)

    def fastForward(self, deltaTime):
        if deltaTime > 0:
            self._updateTime(deltaTime)

    def rewind(self, deltaTime):
        if deltaTime > 0:
            self._updateTime(-deltaTime)

