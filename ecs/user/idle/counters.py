from ecs.core.components.idle import Idle


class UserCounter(Idle):

    # CONSTRUCTOR
    def __init__(self, minVal, maxVal, initVal, hasLimits=True, compName=None):
        super().__init__(compName)
        self._value  = initVal
        self._mini   = minVal
        self._maxi   = maxVal
        self._limits = hasLimits

    # PRIVATE METHODS
    def __saturate(self):
        if self._limits:
            self._value = max(self._mini, min(self._maxi, self._value))

    # SETTERS
    def setMini(self, newMin):
        self._mini = newMin
        self.__saturate()
    def setMaxi(self, newMax):
        self._maxi = newMax
        self.__saturate()
    def setLimits(self,hasLimits):
        self._limits = hasLimits
    def set(self, newVal):
        self._value = newVal
        self.__saturate()
    def modify(self, diff):
        self._value += diff
        self.__saturate()

    # GETTERS
    def getMin(self):
        return self._mini
    def getMax(self):
        return self._maxi
    def hasLimits(self):
        return self._limits
    def getValue(self):
        return self._value
    def getPercent(self):
        return (self._value - self._mini) / (self._maxi - self._mini)

