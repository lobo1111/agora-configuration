from base.Container import Container
from helpers.Label import LabelManager

class Mapper(Container):
    _label = LabelManager()

    def map(self, propertyName, validators):
        for validator in validators:
            validator.validate(self._svars.get(propertyName))
        methodName = "set" + propertyName[0].upper() + propertyName[1:]
        getattr(self._entity, methodName)(self._svars.get(propertyName))
        
    def mapDictionary(self, propertyName, dictionaryValidator):
        entity = dictionaryValidator.validate(self._svars.get(self._svars.get(propertyName + 'Id')))
        methodName = "set" + propertyName[0].upper() + propertyName[1:]
        getattr(self._entity, methodName)(entity)
        
    def setCommunity(self):
        community = self.findById("Community", self._svars.get("communityId"))
        self._entity.setCommunity(community)
        
    def isNew(self):
        return self._isNew
    
    def get(self, property):
        return self._svars.get(property)
    
    def hasAttribute(self, attributeName):
        return attributeName in self._svars
    
    def getEntity(self):
        return self._entity