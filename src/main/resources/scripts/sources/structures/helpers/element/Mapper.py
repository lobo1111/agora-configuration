from pl.reaper.container.data import Element
from pl.reaper.container.data import ElementCommunity
from pl.reaper.container.data import ElementPossession
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.DecimalValidator import DecimalValidator
from structures.validators.common.DictionaryValidator import DictionaryValidator
from structures.validators.common.LengthValidator import LengthValidator

class ElementMapper(Mapper):
    
    def initStructure(self):
        if int(self.get('id')) > 0:
            self._logger.info("Element persist - it's an update. Found id: %s, of type %s" % (self.get('id'), self.get('type')))
            self._entity = self.loadEntity(self.get('type'), int(self.get('id')))
            self._isNew = False
        else:
            self._logger.info("Element persist - it's a new element")
            self._entity = self.initEntity(int(self.get('type')))
            self._isNew = True
            
    def setData(self):
        if self.hasAttribute("algorithm"):
            self.mapDictionary("algorithm", DictionaryValidator(dictionary="ELEMENT_ALGORITHMS", messageParameter = self._label.get('field.algorithm')))
        if self.hasAttribute("group"):
            self.mapDictionary("group", DictionaryValidator(dictionary="ELEMENTS", messageParameter=self._label.get('field.group')))
        if self.hasAttribute("name"):
            self.map("name", [LengthValidator(minLength=1, maxLength=255, messageParameter=self._label.get('field.elementName'))])
        if self.hasAttribute("globalValue"):
            self.map("globalValue", [DecimalValidator(messageParameter=self._label.get('field.value'))])
        if self.hasAttribute("defaultElement"):
            self.map("defaultElement")
        if self.hasAttribute("overrideParentValue"):
            self.map("overrideParentValue")
            
    def loadEntity(self, type, id):
        if type == 'GLOBAL':
            return self.findById("Element", id)
        elif type == 'COMMUNITY':
            return self.findById("ElementCommunity", id)
        elif type == 'POSSESSION':
            return self.findById("ElementPossession", id)
        else:
            return None
        
    def initEntity(self, type):
        if type == 'GLOBAL':
            return Element()
        elif type == 'COMMUNITY':
            return ElementCommunity()
        elif type == 'POSSESSION':
            return ElementPossession()
        else:
            return None