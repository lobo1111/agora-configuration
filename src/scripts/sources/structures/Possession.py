from base.Container import Container
from structures.CommunityDetails import CommunityDetailsManager
from structures.Element import ElementManager
from structures.Zpk import ZpkManager
from structures.helpers.possession.Mapper import PossessionMapper
from structures.helpers.possession.StateCalculator import StateCalculator
from structures.helpers.possession.StateTemplateGenerator import StateTemplateGenerator
from structures.validators.common.ValidationError import ValidationError

class PossessionManager(Container):
    _mapper = PossessionMapper()
    
    def persist(self):
        try:
            self._mapper.initStructure()
            self._mapper.setData()
            if self._mapper.isNew():
                self.createZpkNumbers(self._mapper.getEntity())
                self.createElements(self._mapper.getEntity())
            self._mapper.getEntity().setFullAddress(self._mapper.getEntity().getAddress().getFullAddress())
            CommunityDetailsManager().recalculateShares(self._mapper.getEntity().getCommunity())
            self.saveEntity(self._mapper.getEntity())
        except ValidationError, e:
            self.setError(e)
            
    def createZpkNumbers(self, entity):
        ZpkManager().createZpksForPossession(entity)
    
    def createElements(self, entity):
        ElementManager().createDefaultElementsForPossession(entity)
        
    def getAccountState(self):
        possession = self.findById("Possession", self._svars.get('possessionId'))
        calculator = StateCalculator(possession)
        stateRent, stateRF = calculator.calculateCurrentState()
        chargingRent, chargingRT = calculator.calculateCurrentCharging()
        StateTemplateGenerator().generateTemplate(stateRent, stateRF, chargingRent, chargingRT)
        