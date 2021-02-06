import math

from ecs.core.components.gfx import GfxBurstEmitter
from ecs.core.components.light import LightFx
from ecs.core.components.physic import PhysicCollision
from ecs.core.components.script import Script
from ecs.core.main.entity import Entity
from ecs.user.script.gfxpos import LightFollowGfx
from shmup.common.constants import ZIDX_BUBBLES, ZIDX_OUCH, ZIDX_COINS, ZIDX_HUD
from shmup.factories.coinFactory import CoinFactory
from shmup.factories.dirtyFactory import DirtyFactory


class FishCollisions(Script):


        def __init__(self, entCollide, colTyp1, colTyp2, ePlayers, compName=None):
            # Call to parent
            super().__init__(compName)
            # Create collision components
            cb = {
                "begin"   :self._beginCollision,
                "separate":self._endCollision
            }
            data = {
            }
            collide = PhysicCollision(colTyp1, colTyp2, cb, data)
            entCollide.addComponent(collide)
            # Store player entities
            self._ePlayers = ePlayers
            self._eCollide = entCollide

        def _beginCollision(self, arbiter, space, data):
            for play in self._ePlayers:
                phyComp = play.getComponentsByName("diverPhy")
                if len(phyComp)>0:
                    phyComp = phyComp[0]
                    for bdyShp in phyComp.getBodyList():
                        body = bdyShp[0]
                        shape= bdyShp[1]
                        for contactShape in arbiter.shapes:
                            if contactShape == shape:
                                # player has been found in this contact
                                # make this player lose life
                                lifeComp = play.getComponentsByName("diverLife")[0]
                                lifeComp.modify(-1)
                                # Create burst
                                burstPos = phyComp.getPosition()
                                for i in range(3):
                                    params = {"x0": burstPos[0],
                                              "y0": burstPos[1],
                                              "partSize": 256,
                                              "partScale": 1,
                                              "partSpeed": 3.0,
                                              "lifeTime": 0.20,
                                              "color": (255, 255, 255),
                                              "startAlpha": 100,
                                              "endAlpha": 75 ,
                                              "imagePath": f"resources/images/items/ouch{i}.png",
                                              "partInterval": 0.020,
                                              "totalDuration":0.080,
                                              }
                                    burstComp = GfxBurstEmitter(params, ZIDX_OUCH+i, "OuchEmitter")
                                    # Add burst component to entity
                                    self._eCollide.addComponent(burstComp)

            return True

        def _endCollision(self, arbiter, space, data):
            return True

        def updateScript(self, scriptName, deltaTime):
            pass


class CoinCollisions(Script):

    def __init__(self, entCollide, colTyp1, colTyp2, eCoins, chestScr, scene, compName=None):
        # Call to parent
        super().__init__(compName)
        # Create collision components
        cb = {
            "begin": self._beginCollision,
            "separate": self._endCollision
        }
        data = {
        }
        collide = PhysicCollision(colTyp1, colTyp2, cb, data)
        entCollide.addComponent(collide)
        self._eCollide = entCollide
        self._eCoins = eCoins
        self._chestScr = chestScr
        self._scene = scene

    def _beginCollision(self, arbiter, space, data):
        for coin in self._eCoins:
            phyComp = coin.getComponentsByName("coinPhy")
            if len(phyComp) >= 1:
                phyComp = phyComp[0]
                for bdyShp in phyComp.getBodyList():
                    body  = bdyShp[0]
                    shape = bdyShp[1]
                    for shp in arbiter.shapes:
                        if shp == shape:
                            # We have found a coin here destory it
                            self._eCoins.remove(coin)
                            coin.destroy()
                            # Create burst emitter at the physic position of the fish
                            burstPos = phyComp.getPosition()
                            params = {"x0": burstPos[0],
                                      "y0": burstPos[1],
                                      "partSize": 128,
                                      "partScale": 0.5,
                                      "partSpeed": 0.0,
                                      "lifeTime": 0.25,
                                      "color": (255, 255, 0),
                                      "startAlpha": 100,
                                      "endAlpha": 25,
                                      "imagePath": "resources/images/items/coin.png",
                                      "partInterval": 0.02,
                                      "totalDuration": 0.5,
                                      }
                            burstComp = GfxBurstEmitter(params, ZIDX_HUD-100, "coinEmitter")
                            light = LightFx(burstPos, 48,(255,255,0),"soft")
                            lightEntity = Entity()
                            lightFollow = LightFollowGfx(burstComp, light, lightEntity)
                            lightEntity.addComponent(light)
                            lightEntity.addComponent(lightFollow)
                            self._scene.addEntity(lightEntity)
                            # Add it into the entity for coin burst
                            self._eCollide.addComponent(burstComp)
                            # Add this into the script to move coins
                            self._chestScr.insertCoin(burstComp)
                            return True
        return True

    def _endCollision(self, arbiter, space, data):
        return True

    def updateScript(self, scriptName, deltaTime):
        pass


class DirtyCollisions(Script):

    def __init__(self, entCollide, colTyp1, colTyp2, eDirty, trashScr, scene, compName=None):
        # Call to parent
        super().__init__(compName)
        # Create collision components
        cb = {
            "begin": self._beginCollision,
            "separate": self._endCollision
        }
        data = {
        }
        collide = PhysicCollision(colTyp1, colTyp2, cb, data)
        entCollide.addComponent(collide)
        self._eCollide = entCollide
        self._eDirty = eDirty
        self._trashScr = trashScr
        self._scene = scene

    def _beginCollision(self, arbiter, space, data):
        for dirt in self._eDirty:
            phyComp = dirt.getComponentsByName("dirtyPhy")
            if len(phyComp) >= 1:
                phyComp = phyComp[0]
                for bdyShp in phyComp.getBodyList():
                    body  = bdyShp[0]
                    shape = bdyShp[1]
                    for shp in arbiter.shapes:
                        if shp == shape:
                            typeCmp = dirt.getComponentsByName("dirtType")
                            type  = 0
                            if len(typeCmp) >= 1:
                                type = typeCmp[0].getValue()
                            # We have found a dirty here destory it
                            self._eDirty.remove(dirt)
                            dirt.destroy()
                            # Create burst emitter at the physic position of the fish
                            burstPos = phyComp.getPosition()
                            params = {"x0": burstPos[0],
                                      "y0": burstPos[1],
                                      "partSize": 128,
                                      "partScale": 0.7,
                                      "partSpeed": 0.0,
                                      "lifeTime": 0.25,
                                      "color": (255, 255, 255),
                                      "startAlpha": 100,
                                      "endAlpha": 25,
                                      "partInterval": 0.02,
                                      "totalDuration": 0.5,
                                      }
                            data = DirtyFactory.DIRTS[type]
                            params["imagePath"] = data["filePath"]
                            burstComp = GfxBurstEmitter(params, ZIDX_HUD-100, "dirtyEmitter")
                            light = LightFx(burstPos, 60, (255, 16, 0), "soft")
                            lightEntity = Entity()
                            lightFollow = LightFollowGfx(burstComp, light, lightEntity)
                            lightEntity.addComponent(light)
                            lightEntity.addComponent(lightFollow)
                            self._scene.addEntity(lightEntity)
                            # Add it into the entity for coin burst
                            self._eCollide.addComponent(burstComp)
                            # Add this into the script to move coins
                            self._trashScr.insertTrash(burstComp)
                            return True
        return True

    def _endCollision(self, arbiter, space, data):
        return True

    def updateScript(self, scriptName, deltaTime):
        pass



class BubbleCollisions(Script):

    def __init__(self, entCollide, colTyp1, colTyp2, eFishes, eBubbles, eCoins, compName=None):
        # Call to parent
        super().__init__(compName)
        # Create collision components
        cb = {
            "begin": self._beginCollision,
            "separate": self._endCollision
        }
        data = {
        }
        collide = PhysicCollision(colTyp1, colTyp2, cb, data)
        entCollide.addComponent(collide)
        # Store entity lists
        self._eFishes  = eFishes
        self._eBubbles = eBubbles
        self._eCoins   = eCoins
        self._eCollide = entCollide


    def _beginCollision(self, arbiter, space, data):
        # Entities to destroy
        toDestroy = []

        # Look for fishes in collisions
        for fish in self._eFishes:
            phyComp = fish.getComponentsByName("fishPhy")
            if len(phyComp) >= 1:
                phyComp = phyComp[0]
                for bdyShp in phyComp.getBodyList():
                    body  = bdyShp[0]
                    shape = bdyShp[1]

                    # find fish shape
                    idxFish       = -1
                    idxBubble     = -1
                    if arbiter.shapes[0] == shape:
                        idxFish   = 0
                        idxBubble = 1
                    if arbiter.shapes[1] == shape:
                        idxFish   = 1
                        idxBubble = 0
                    # A contact has been found
                    if idxFish != -1 and idxBubble != -1:
                        # Get bubble body from shape
                        bdyBubble = arbiter.shapes[idxBubble].body
                        bubVel = bdyBubble.velocity
                        # compte angle
                        bubAng = 180*math.atan2(bubVel[1], bubVel[0])/math.pi
                        if abs(bubAng) < 30:
                            # Here we have found a collision between fish and bubble
                            # and the bubble orientation is correct to "hit" the fish

                            # decrease fish life and destroy if it reaches zero
                            lifeCmp = fish.getComponentsByName("fishLife")
                            if len(lifeCmp)>=1:
                                lifeCmp = lifeCmp[0]
                            lifeCmp.modify(-1)
                            # make this fish entity disappear if life is 0
                            if lifeCmp.getValue() <= 0:
                                toDestroy.append(fish)
                                # Create burst emitter at the physic position of the fish
                                burstPos = phyComp.getPosition()
                                params = {"x0": burstPos[0],
                                          "y0": burstPos[1],
                                          "partSize": 128,
                                          "partScale": 0.75,
                                          "partSpeed": 7.0,
                                          "lifeTime": 0.4,
                                          "color": (0, 0, 255),
                                          "startAlpha": 100,
                                          "endAlpha": 50,
                                          "imagePath": "resources/images/items/bubble.png",
                                          "partInterval": 0.010,
                                          "totalDuration":0.100,
                                          }
                                burstComp = GfxBurstEmitter(params, ZIDX_BUBBLES, "BurstEmitter")
                                # Add burst component to entity
                                self._eCollide.addComponent(burstComp)
                                # Create gold coin
                                coin = CoinFactory().create(burstPos, self._eCoins)
                                scene = self._eCollide.getScene()
                                if scene != None:
                                    scene.addEntity(coin)
                                    self._eCoins.append(coin)


        # Look for bubbles in collisions
        for bubble in self._eBubbles:
            phyComp = bubble.getComponentsByName("bubblePhy")
            if len(phyComp) >= 1:
                phyComp = phyComp[0]
                for bdyShp in phyComp.getBodyList():
                    body = bdyShp[0]
                    shape = bdyShp[1]

                    # find fish shape
                    idxFish       = -1
                    idxBubble     = -1
                    if arbiter.shapes[0] == shape:
                        idxFish   = 1
                        idxBubble = 0
                    if arbiter.shapes[1] == shape:
                        idxFish   = 0
                        idxBubble = 1
                    # A contact has been found
                    if idxFish != -1 and idxBubble != -1:
                        # Get bubble body from shape
                        bdyBubble = arbiter.shapes[idxBubble].body
                        bubVel = bdyBubble.velocity
                        # compte angle
                        bubAng = 180*math.atan2(bubVel[1], bubVel[0])/math.pi
                        if abs(bubAng) < 30:
                            # Here we have found a collision between fish and bubble
                            # and the bubble orientation is correct to "hit" the fish

                            # make this bubble entity disappear
                            toDestroy.append(bubble)
                            # Get player score component
                            score = phyComp.getUserData("score")
                            if score != None:
                                # increase score
                                score.modify(1)


        # Now destroy all of them
        for entity in toDestroy:
            entity.destroy()

        # Do not process collision
        return False



    def _endCollision(self, arbiter, space, data):
        return True

    def updateScript(self, scriptName, deltaTime):
        pass

