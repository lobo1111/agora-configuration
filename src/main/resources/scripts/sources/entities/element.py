from pl.reaper.container.data import Element
from pl.reaper.container.data import ElementCommunity
from pl.reaper.container.data import ElementPossession

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
    
    def addDefaultElements(self, community):
        for element in self.findDefaultElements():
            vars.put("elementId", element.getId())
            self.CreateOrUpdateCommunityElement(community)
    
    def remove(self):
        element = self.findElementById(vars.get('id'))
        entityManager.remove(element)
        
    def removeSubElement(self):
        if vars.get('subType') == "COMMUNITY":
            element = self.findSubElementCommunity(vars.get('subId'))
            self._logger.info('Removing community element - %d' % element.getId())
            for possessionElement in element.getPossessionsElements():
                if not possessionElement.isOverrideParentValue():
                    entityManager.remove(possessionElement)
                    self._logger.info('Removing possession element - %d' % possessionElement.getId())
                else:
                    possessionElement.setElementCommunity(None)
                    self.saveElement(possessionElement)
                    self._logger.info('Possession element not removued due to override flag set - %d' % possessionElement.getId())
            entityManager.remove(element)
        elif vars.get('subType') == "POSSESSION":
            element = self.findSubElementPossession(vars.get('subId'))
            self._logger.info('Removing possession element - %d' % element.getId())
            entityManager.remove(element)
        
    def CreateOrUpdateCommunityElement(self, community):
        elementId = vars.get("elementId")
        communityId = community.getId()
        communityElement = self.findCommunityElement(elementId, communityId)
        createElementForPossessions = False
        if communityElement is None:
            communityElement = ElementCommunity()
            createElementForPossessions = True
            communityElement.setElement(self.findElementById(elementId))
            communityElement.setCommunity(community)
        if vars.get('override') == 'true':
            communityElement.setOverrideParentValue(True)
        else:
            communityElement.setOverrideParentValue(False)
        communityElement.setGlobalValue(float(vars.get("overrideValue")))
        if createElementForPossessions:
            tmpOverride = vars.get('override')
            tmpOverrideValue = vars.get("overrideValue")
            self.setElementForPossessions(community, communityElement)
            vars.put('override', tmpOverride)
            vars.put('overrideValue', tmpOverrideValue)
        self.saveElement(communityElement)
        
    def setElementForPossessions(self, community, communityElement):
        for possession in community.getPossessions():
            vars.put("overrideValue", "0")
            vars.put("override", "false")
            self.CreateOrUpdatePossessionElement(possession, communityElement, False)
            
    def CreateOrUpdatePossessionElement(self, possession, elementCommunity = None, override = True):
        elementId = vars.get("elementId")
        possessionId = possession.getId()
        possessionElement = self.findPossessionElement(elementId, possessionId)
        if possessionElement is None:
            possessionElement = ElementPossession()
            possessionElement.setElementCommunity(elementCommunity)
            possessionElement.setElement(self.findElementById(elementId))
            possessionElement.setPossession(possession)
        if not elementCommunity is None:
            possessionElement.setElementCommunity(elementCommunity)
        if override:
            if vars.get('override') == 'true':
                possessionElement.setOverrideParentValue(True)
            else:
                possessionElement.setOverrideParentValue(False)
            possessionElement.setGlobalValue(float(vars.get('overrideValue')))
        self.saveElement(possessionElement)
            
    def setElementData(self, element):
        element.setName(vars.get(self._prefix + 'name'))
        element.setKey(vars.get(self._prefix + 'key'))
        element.setGlobalValue(BigDecimal(vars.get(self._prefix + 'value')).floatValue())
        element.setGroup(self.findGroupById(vars.get(self._prefix + 'groupId')))
        if vars.get(self._prefix + 'defaultValue') == 'true':
            element.setDefaultElement(True)
        else:
            element.setDefaultElement(False)
        element.setAlgorithm(vars.get(self._prefix + 'algorithm'))
        
    def saveElement(self, element):
        entityManager.persist(element)
        entityManager.flush()
        
    def findElementById(self, id):
        return entityManager.createQuery('Select element From Element element Where element.id = ' + id).getSingleResult()
        
    def findSubElementCommunity(self, id):
        return entityManager.createQuery('Select element From ElementCommunity element Where element.id = ' + id).getSingleResult()
        
    def findSubElementPossession(self, id):
        return entityManager.createQuery('Select element From ElementPossession element Where element.id = ' + id).getSingleResult()
    
    def findCommunityElement(self, elementId, communityId):
        try:
            return entityManager.createQuery('Select element From ElementCommunity element join element.element parent join element.community community Where parent.id = %s and community.id = %s' % (elementId, communityId)).getSingleResult()
        except:
            return None
    
    def findPossessionElement(self, elementId, possessionId):
        try:
            return entityManager.createQuery('Select element From ElementPossession element join element.element parent join element.possession possession Where parent.id = %s and possession.id = %s' % (elementId, possessionId)).getSingleResult()
        except:
            return None
    
    def findGroupById(self, id):
        return entityManager.createQuery('Select dict From Dictionary dict Where dict.id = ' + id).getSingleResult()
    
    def findDefaultElements(self):
        return entityManager.createQuery('Select element From Element element where element.defaultElement = 1').getResultList()