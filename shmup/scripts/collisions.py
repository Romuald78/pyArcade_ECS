from ecs.core.components.physic import PhysicCollision
from ecs.core.components.script import Script


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



        def _beginCollision(self, arbiter, space, data):
            for play in self._ePlayers:
                phyComp = play.getComponentsByName("diverPhy")[0]
                for bdyShp in phyComp.getBodyList():
                    body = bdyShp[0]
                    shape= bdyShp[1]
                    for contactShape in arbiter.shapes:
                        if contactShape == shape:
                            # player has been found in this contact
                            # make this player lose life
                            lifeComp = play.getComponentsByName("diverLife")[0]
                            lifeComp.modify(-1)
                            lifeText = play.getComponentsByName("lifeText")[0]
                            lifeText.setMessage(str(lifeComp.getValue()))
            return True

        def _endCollision(self, arbiter, space, data):
            return True

        def updateScript(self, scriptName, deltaTime):
            pass
