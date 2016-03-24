from base.Container import Container
from helpers.Label import LabelManager

class Mapper(Container):
    _label = LabelManager()

    def map(self, propertyName, validators = [], mappedEntity = None):
        if mappedEntity == None:
            mappedEntity = self._entity
        for validator in validators:
            validator.validate(self._svars.get(propertyName))
        methodName = "set" + propertyName[0].upper() + propertyName[1:]
        if self._svars.get(propertyName + "Type") == 'javafx.beans.property.SimpleIntegerProperty':
            getattr(mappedEntity, methodName)(self._svars.get(propertyName))
            self._logger.info("Mapped %s=%s as Integer" % (propertyName, self._svars.get(propertyName)))
        if self._svars.get(propertyName + "Type") == 'javafx.beans.property.SimpleStringProperty':
            getattr(mappedEntity, methodName)(self._svars.get(propertyName))
            self._logger.info("Mapped %s=%s as String" % (propertyName, self._svars.get(propertyName)))
        if self._svars.get(propertyName + "Type") == 'javafx.beans.property.SimpleDoubleProperty':
            getattr(mappedEntity, methodName)(float(self._svars.get(propertyName)))
            self._logger.info("Mapped %s=%s as Double" % (propertyName, self._svars.get(propertyName)))
        if self._svars.get(propertyName + "Type") == 'javafx.beans.property.SimpleBooleanProperty':
            getattr(mappedEntity, methodName)(self._svars.get(propertyName) == 'true')
            self._logger.info("Mapped %s=%s as Boolean" % (propertyName, self._svars.get(propertyName)))
            
        
    def mapDictionary(self, propertyName, dictionaryValidator, mappedEntity = None):
        if mappedEntity == None:
            mappedEntity = self._entity
        entity = dictionaryValidator.validate(self._svars.get(propertyName + 'Id'))
        methodName = "set" + propertyName[0].upper() + propertyName[1:]
        getattr(mappedEntity, methodName)(entity)
        
    def mapDate(self, propertyName, validators, mappedEntity = None):
        if mappedEntity == None:
            mappedEntity = self._entity
        date = self.parseDate(self.get(propertyName))
        for validator in validators:
            validator.validate(date)
        methodName = "set" + propertyName[0].upper() + propertyName[1:]
        getattr(mappedEntity, methodName)(date)
    
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