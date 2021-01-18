

class Entity():

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self):
        # init component list
        self.__components = {}


    ## -------------------------------------
    ## Component management
    ## -------------------------------------
    # TODO WARNING :
    # adding a component in an entity
    # AFTER an entity has been added to
    # the world, makes this component
    # not included !!
    def addComponent(self, cmpName, cmpRef):
        if cmpName not in self.__components:
            self.__components[cmpName] = cmpRef

    def getNbComponents(self):
        return len(self.__components)

    def getComponent(self, cmpName):
        res = None
        if cmpName in self.__components:
            res = self.__components[cmpName]
        return res

    def getAllComponents(self):
        return dict(self.__components)
