# TODO FEATURE : add remove method and link to the different systems ?
# May be an easier way is to go via Entity : destroy request sent to the scene
# So the access to the systems can be done

# TODO WARNING :
# adding a component in an entity
# AFTER an entity has been added to
# the world, makes this component
# not included !!

class Entity():

    #---------------------------------------------
    # COMPONENT ID
    #---------------------------------------------
    # Static field
    _maxEntID = 0
    @staticmethod
    def getNewID():
        Entity._maxEntID += 1
        return Entity._maxEntID


    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self, entName=None):
        self._ID = Entity.getNewID()
        if entName == None:
            entName = "ENTITY"
        self._name = f"e_{entName}_{self._ID}"
        # init component list
        self._compByName = {}
        self._compByRef  = {}

    # ---------------------------------------------
    # GETTERS
    # ---------------------------------------------
    def getName(self):
        return self._name

    def getID(self):
        return self._ID

    ## -------------------------------------
    ## Component management
    ## -------------------------------------
    def addComponent(self, cmpRef):
        # Get name of this component
        cmpName = cmpRef.getName()
        # Add ref into NAME dict
        if cmpName not in self._compByName:
            self._compByName[cmpName] = []
        if cmpRef in self._compByName[cmpName]:
            raise ValueError("[ERR] addComponent : ref is already in the name dict !")
        self._compByName[cmpName].append(cmpRef)
        # Add name into REF dict
        if cmpRef in self._compByRef:
            raise ValueError("[ERR] addComponent : ref is already in the ref dict !")
        self._compByRef[cmpRef] = cmpName

    def getNbComponents(self):
        return len(self._compByRef)

    def getComponentsByName(self, cmpName):
        res = []
        if cmpName in self._compByName:
            res = self._compByName[cmpName]
        return res

    def hasComponent(self, cmpRef):
        return cmpRef in self._compByRef

    def getComponentList(self):
        return list(self._compByRef.keys())

