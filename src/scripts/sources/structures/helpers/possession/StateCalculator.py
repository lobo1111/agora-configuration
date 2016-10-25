from base.Container import Container

class StateCalculator(Container):
    
    def __init__(self, possession):
        self._possession = possession
    
    def calculateCurrentState(self):
        return 0, 0
    
    def calculateCurrentCharging(self):
        return 0, 0