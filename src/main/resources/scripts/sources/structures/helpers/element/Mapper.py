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
            self._entity = self.initEntity(self.get('type'))
            self._isNew = True
            
    def setData(self):
        if self.get('type') == 'GLOBAL':
            self.mapDictionary("algorithm", DictionaryValidator(dictionary="ELEMENT_ALGORITHMS", messageParameter = self._label.get('field.algorithm')))
            self.mapDictionary("group", DictionaryValidator(dictionary="ELEMENTS", messageParameter=self._label.get('field.group')))
            self.map("name", [LengthValidator(minLength=1, maxLength=255, messageParameter=self._label.get('field.elementName'))])
            self.map("defaultElement")
        if self.get('type') == 'COMMUNITY' or self.get('type') == 'POSSESSION':
            self.map("overrideParentValue")
        self.map("globalValue", [DecimalValidator(messageParameter=self._label.get('field.value'))])
            
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