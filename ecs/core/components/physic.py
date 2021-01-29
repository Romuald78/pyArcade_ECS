
## ============================================================
## IMPORTS
## ============================================================
import arcade
import pymunk

from ecs.core.components.component import Component



## ============================================================
## PHYSIC COMPONENT
## ============================================================

# TODO Handle Kinematic, Static, ...
from ecs.core.components.script import Script


class Physic(Component):

    # constructor
    def __init__(self, compName=None):
        if compName == None :
            compName = "USER"
        super().__init__(compName)
        # Init fields
        self._sensor          = False            # Sensor means, just collision detection, no physic
        self._bodiesAndShapes = []      # tuple with (1-body,1-shape)

    # method to get current type
    def getType(self):
        raise ValueError("Physic : getType method has not been implemented yet !")

    # Body management
    def getNbBodies(self):
        return len(self._bodiesAndShapes)

    def getBodyList(self):
        return self._bodiesAndShapes

    def drawDebug(self):
        raise ValueError("[ERR] Physic drawDebug method has not been implemented yet !")

    # Position
    def getPosition(self):
        pos  = self._bodiesAndShapes[0][0].position
        return pos
    def setPosition(self, pos):
        self._bodiesAndShapes[0][0].position = pos

    # Velocity
    def getVelocity(self):
        return self._bodiesAndShapes[0][0].velocity

    def setVelocity(self,vel):
        self._bodiesAndShapes[0][0].velocity = vel

    # Angle
    def getAngle(self):
        return self._bodiesAndShapes[0][0].angle

    def setAngle(self, ang):
        self._bodiesAndShapes[0][0].angle = ang


    # movement
    def applyImpulse(self, dx, dy):
        vect = (dx,dy)
        return self._bodiesAndShapes[0][0].apply_impulse_at_local_point(vect)

    # Sensor management
    def enableSensor(self):
        shape = self._bodiesAndShapes[0][1]
        shape.sensor = True

    def disableSensor(self):
        shape = self._bodiesAndShapes[0][1]
        shape.sensor = False

    def isSensor(self):
        shape = self._bodiesAndShapes[0][1]
        return shape.sensor

    def getCollisionType(self):
        shape = self._bodiesAndShapes[0][1]
        return shape.collision_type


class PhysicBox(Physic):

    def __init__(self, params, compName=None):
        if compName == None:
            compName = "PHYSIC_BOX"
        # Call to constructor
        super().__init__(compName)
        # Retrieve data from params
        mass   = params["mass"]
        size   = params["size"]
        mode   = params["mode"]
        pos    = params["pos"]
        moment = 1
        # Create body, shape, and set the position
        body  = pymunk.Body(mass,moment,mode)
        shape = pymunk.Poly.create_box(body,size)
        print(f"[Body @{body} / Shape @{shape}")
        body.position = pos
        # Store info into list (tuple : body, shape)
        self._bodiesAndShapes.append((body,shape))

    def getType(self):
        return Component.TYPE_PHYSIC_BOX


class PhysicDisc(Physic):

    def __init__(self, params, compName=None):
        if compName == None:
            compName = "PHYSIC_BOX"
        # Call to constructor
        super().__init__(compName)
        # Retrieve data from params
        mass   = params["mass"]
        radius = params["radius"]
        mode   = params["mode"]
        pos    = params["pos"]
        sensor = params["sensor"]
        colTyp = params["collisionType"]
        # Create body, shape, and set the position
        inertia       = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body          = pymunk.Body(mass, inertia, mode)
        body.position = pos
        shape                = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity     = 0.5
        shape.friction       = 2
        shape.collision_type = colTyp
        shape.sensor         = sensor
        # Store info into list (tuple : body, shape)
        self._bodiesAndShapes.append((body,shape))
        self._radius = radius

    def getType(self):
        return Component.TYPE_PHYSIC_DISC

    def drawDebug(self):
        xc,yc = self.getPosition()
        arcade.draw_circle_outline(xc,yc,self.getRadius(),(255,255,255))

    def getRadius(self):
        return self._radius


class PhysicCollision(Script):

    def __init__(self, colTyp1, colTyp2, callbacks, data, compName=None):
        # Call to parent
        super().__init__(compName)
        # Store handler fields
        self._typ1      = colTyp1
        self._typ2      = colTyp2
        self._callbacks = callbacks
        self._data      = data
        self._isStarted = False

    def updateScript(self, scriptName, deltaTime):
        # Start collision handler as soon as possible
        if not self._isStarted:
            entity = self.getEntity()
            if entity != None:
                scene = entity.getScene()
                if scene != None:
                    scene.addCollisionHandler(self._typ1, self._typ2, self._callbacks, self._data)
                    self._isStarted = True

    # Callback names are "begin", "separate"
    # Their signature contains (arbiter, space, data)

    def stop(self):
        if self._isStarted:
            raise ValueError("[ERR] PhysicCollision 'stop' method has not been implemented yet !")

