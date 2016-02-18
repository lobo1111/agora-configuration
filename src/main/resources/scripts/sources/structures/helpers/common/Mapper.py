from base.Container import Container

class Mapper(Container):
    def map(self, propertyName, validators):
        for validator in validators:
            validator.validate(self._svars.get(propertyName))
        methodName = "set" + propertyName[0].upper() + propertyName[1:]
        getattr(self._entity, methodName)(self._svars.get(propertyName))
        
    def setCommunity(self):
        community = self.findById("Community", self._svars.get("communityId"))
        self._entity.setCommunity(community)
        
    def isNew(self):
        return self._isNew
    
    def get(self, property):
        return self._svars.get(property)
    
    def getEntity(self):
        return self._entity