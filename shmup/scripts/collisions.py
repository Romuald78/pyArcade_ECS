from ecs.core.components.gfx import GfxBurstEmitter
from ecs.core.components.physic import PhysicSensor
from ecs.core.components.script import Script
from shmup.common.constants import Z_INDEX_STARS


class FoxGame(Script):

    def __init__(self, entGame, playerList, entBurst, foxGfx, compName=None):
        if compName == None:
            compName = "FoxGame"
        # parent call
        super().__init__(compName)
        # Store fields
        self._lastHitDuration = 0
        self._entBurst  = entBurst
        self._sensors   = []
        self._gfxs      = []
        self._fox       = 0        # first player is the Fox by default
        self._foxGfx    = foxGfx

        # Prepare Sensors from physic components
        for i in range(len(playerList)):
            # Store gfx for updateScript
            gfx1 = playerList[i].getComponentsByName("shipGfx")[0]
            self._gfxs.append(gfx1)
            for j in range(i+1,len(playerList)):
                phy1    = playerList[i].getComponentsByName("shipPhy")[0]
                phy2    = playerList[j].getComponentsByName("shipPhy")[0]
                colTyp1 = phy1.getCollisionType()
                colTyp2 = phy2.getCollisionType()
                # Create sensor component
                collide = PhysicSensor(colTyp1, colTyp2, f"Sensor{i}{j}")
                # Add it to the sensor list (storing player index too)
                self._sensors.append({"collRef":collide,
                                      "playerIndex1":i,
                                      "playerIndex2":j
                                      })
                # Add collision component to entity
                entGame.addComponent(collide)

    def updateScript(self, scriptName, deltaTime):
        # update last hit
        if self._lastHitDuration < 1:
            self._lastHitDuration += deltaTime
        else:
            # Check all sensors
            for sensor in self._sensors:
                # Get info from sensor
                collComp = sensor["collRef"]
                idxP1    = sensor["playerIndex1"]
                idxP2    = sensor["playerIndex2"]
                # check if collision is ON
                if collComp.hasBeenActivated():
                    # Get positions of both players
                    x1, y1 = self._gfxs[idxP1].getPosition()
                    x2, y2 = self._gfxs[idxP2].getPosition()
                    # init burst creation flag
                    isNewFox = False
                    # P1 was the fox
                    if self._fox == idxP1:
                        # Now it is P2
                        self._fox = idxP2
                        isNewFox  = True
                    # P2 was the fox
                    elif self._fox == idxP2:
                        # Now it is P1
                        self._fox = idxP1
                        isNewFox  = True
                    # Create burst if needed
                    if isNewFox:
                        print(f"New Fox {self._fox}")
                        # Prepare params for burst emitter
                        params  = {"x0"           : (x1+x2)/2,
                                   "y0"           : (y1+y2)/2,
                                   "partSize"     : 32,
                                   "partScale"    : 1.5,
                                   "partSpeed"    : 2.0,
                                   "color"        : (255, 255, 0),
                                   "startAlpha"   : 100,
                                   "endAlpha"     : 50,
                                   "imagePath"    : "resources/images/items/star.png",
                                   "partInterval" : 0.070,
                                   "totalDuration": 0.30
                                   }
                        starBurst = GfxBurstEmitter(params,Z_INDEX_STARS,"starBurst")
                        self._entBurst.addComponent(starBurst)
                        # reinit timer and collision
                        self._lastHitDuration = 0

        # Place fox Gfx to current fox position
        foxPos = self._gfxs[self._fox].getPosition()
        self._foxGfx.setPosition(foxPos)



