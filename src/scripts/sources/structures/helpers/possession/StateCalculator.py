from base.Container import Container

class StateCalculator(Container):
    
    def __init__(self, possession):
        self._possession = possession
    
    def calculateCurrentRentState(self):
        return 1
    
    def calculateCurrentRFState(self):
        return 1
    
    def calculateRentCharging(self):
        return 1
    
    def calculateRFCharging(self):
        return 1