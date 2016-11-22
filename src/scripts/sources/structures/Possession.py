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
            self.createZpkNumbers(self._mapper.getEntity())
            if self._mapper.isNew():
                self.createElements(self._mapper.getEntity())
            self.saveEntity(self._mapper.getEntity())
            self.refreshShortcuts(self._mapper.getEntity())
            CommunityDetailsManager().recalculateShares(self._mapper.getEntity().getCommunity())
        except ValidationError, e:
            self.setError(e)
            
    def createZpkNumbers(self, entity):
        ZpkManager().createZpksForPossession(entity)
    
    def createElements(self, entity):
        ElementManager().createDefaultElementsForPossession(entity)
        
    def getAccountState(self):
        possession = self.findById("Possession", self._svars.get('possessionId'))
        calculator = StateCalculator()
        calculator.setPossession(possession)
        StateTemplateGenerator().generateTemplate(calculator)

    def refreshShortcuts(self, possession):
        owners = possession.getOwnersAsString()
        possession.setOwnersNames(owners)
        possession.setFullAddress(possession.getAddress().getFullAddress())
        possession.setFullAddressWithNames(possession.getFullAddress() + " - " + possession.getOwnersNames())
        