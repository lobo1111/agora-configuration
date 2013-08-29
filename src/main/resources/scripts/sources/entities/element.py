from pl.reaper.container.data import Element

from java.math import BigDecimal

class ElementManager(Container):
    _logger = Logger([:_scriptId])
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix
    
    def create(self):
        element = Element()
        self.setElementData(element)
        self.saveElement(element)
        return element
        
    def update(self):
        element = self.findElementById(vars.get(self._prefix + 'id'))
        self.setElementData(element)
        self.saveElement(element)
        return element
        
    def setElementData(self, element):
        element.setName(vars.get(self._prefix + 'name'))
        element.setKey(vars.get(self._prefix + 'key'))
        element.setGlobalValue(BigDecimal(vars.get(self._prefix + 'value')).floatValue())
        element.setGroup(self.findGroupById(vars.get(self._prefix + 'groupId')))
        
    def saveElement(self, element):
        entityManager.persist(element)
        entityManager.flush()
        
    def findElementById(self, id):
        return entityManager.createQuery('Select element From Element element Where element.id = ' + id).getSingleResult()
    
    def findGroupById(self, id):
        return entityManager.createQuery('Select dict From Dictionary dict Where dict.id = ' + id).getSingleResult()