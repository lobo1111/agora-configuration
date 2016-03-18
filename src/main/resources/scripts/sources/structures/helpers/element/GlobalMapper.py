from pl.reaper.container.data import Element
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.DecimalValidator import DecimalValidator
from structures.validators.common.DictionaryValidator import DictionaryValidator
from structures.validators.common.LengthValidator import LengthValidator

class GlobalMapper(Mapper):
    _specializedMapper = None
    
    def initStructure(self):
        if self.nameAlreadyExists():
            self.loadEntity()
        else:
            self.newEntity()
        if self._specializedMapper != None:
            self._specializedMapper.initStructure()
            self._specializedMapper.bind(self._entity)
    
    def newEntity(self):
        self._isNew = True
        self._entity = Element()
    
    def loadEntity(self):
        self._isNew = False
        self._entity = self.findById("Element", self._svars.get('id'))
        
    def nameAlreadyExists(self):
        self.findBy("Element", "'name'", self._svars.get('name')) != None
    
    def setSpecializedMapper(self, specializedMapper):
        self._specializedMapper = specializedMapper
        
    def getSpecializedMapper(self):
        return self._specializedMapper
    
    def setData(self):
        if self._specializedMapper != None:
            self._specializedMapper.setData()
        if self._specializedMapper == None or self._isNew:
            self.map("defaultElement")
            self.map("name", [LengthValidator(minLength=1, maxLength=255, messageParameter=self._label.get('field.elementName'))])
            self.mapDictionary("group", DictionaryValidator(dictionary="ELEMENTS", messageParameter=self._label.get('field.group')))
            self.mapDictionary("algorithm", DictionaryValidator(dictionary="ELEMENT_ALGORITHMS", messageParameter = self._label.get('field.algorithm')))
            self.map("globalValue", [DecimalValidator(messageParameter=self._label.get('field.value'))])
    
    