from pl.reaper.container.data import Element
from pl.reaper.container.data import ElementCommunity
from pl.reaper.container.data import ElementPossession
from base.Container import Container

from java.math import BigDecimal

class ElementManager(Container):
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix
    
    def create(self):
        element = Element()
        self.setElementData(element)
        self.saveElement(element)
        return element
        
    def update(self):
        global svars
        element = self.findElementById(svars.get(self._prefix + 'id'))
        self.setElementData(element)
        self.saveElement(element)
        return element
    
    def addDefaultElements(self, community):
        global svars
        for element in self.findDefaultElements():
            self._logger.info('Adding default community element - %d' % element.getId())
            svars.put("elementId", element.getId())
            self.CreateOrUpdateCommunityElement(community)
    
    def remove(self):
        global svars
        element = self.findElementById(svars.get('id'))
        entityManager.remove(element)
        
    def removeSubElement(self):
        global svars
        if svars.get('subType') == "COMMUNITY":
            element = self.findSubElementCommunity(svars.get('subId'))
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
        elif svars.get('subType') == "POSSESSION":
            element = self.findSubElementPossession(svars.get('subId'))
            self._logger.info('Removing possession element - %d' % element.getId())
            entityManager.remove(element)
        
    def CreateOrUpdateCommunityElement(self, community):
        global svars
        elementId = svars.get("elementId")
        communityId = community.getId()
        communityElement = self.findCommunityElement(elementId, communityId)
        createElementForPossessions = False
        if communityElement is None:
            communityElement = ElementCommunity()
            createElementForPossessions = True
            communityElement.setElement(self.findElementById(elementId))
            communityElement.setCommunity(community)
            community.getElements().add(communityElement)
        if svars.get('override') == 'true':
            communityElement.setOverrideParentValue(True)
        else:
            communityElement.setOverrideParentValue(False)
        if not svars.get("overrideValue") is None and not svars.get("overrideValue") == '':
            communityElement.setGlobalValue(float(svars.get("overrideValue")))
        if createElementForPossessions:
            tmpOverride = svars.get('override')
            tmpOverrideValue = svars.get("overrideValue")
            self.setElementForPossessions(community, communityElement)
            svars.put('override', tmpOverride)
            svars.put('overrideValue', tmpOverrideValue)
        entityManager.persist(community)
        self.saveElement(communityElement)
        
    def setElementForPossessions(self, community, communityElement):
        global svars
        for possession in community.getPossessions():
            svars.put("overrideValue", "0")
            svars.put("override", "false")
            self.CreateOrUpdatePossessionElement(possession, communityElement, False)
            
    def propagateElementsForNewPossession(self, possession):
        global svars
        for communityElement in possession.getCommunity().getElements():
            self._logger.info('Propagating element for new possession - %d' % communityElement.getElement().getId())
            svars.put("elementId", str(communityElement.getElement().getId()))
            self.CreateOrUpdatePossessionElement(possession, communityElement, False)
            
    def CreateOrUpdatePossessionElement(self, possession, elementCommunity = None, override = True):
        global svars
        elementId = svars.get("elementId")
        possessionId = possession.getId()
        possessionElement = self.findPossessionElement(elementId, possessionId)
        if possessionElement is None:
            possessionElement = ElementPossession()
            possessionElement.setElementCommunity(elementCommunity)
            possessionElement.setElement(self.findElementById(elementId))
            possessionElement.setPossession(possession)
            possession.getElements().add(possessionElement)
        if not elementCommunity is None:
            possessionElement.setElementCommunity(elementCommunity)
        if override:
            if svars.get('override') == 'true':
                possessionElement.setOverrideParentValue(True)
            else:
                possessionElement.setOverrideParentValue(False)
            possessionElement.setGlobalValue(float(svars.get('overrideValue')))
        entityManager.persist(possession)
        self.saveElement(possessionElement)
            
    def setElementData(self, element):
        global svars
        element.setName(svars.get(self._prefix + 'name'))
        element.setKey(svars.get(self._prefix + 'key'))
        element.setGlobalValue(BigDecimal(svars.get(self._prefix + 'value')).floatValue())
        element.setGroup(self.findGroupById(svars.get(self._prefix + 'groupId')))
        if svars.get(self._prefix + 'defaultValue') == 'true':
            element.setDefaultElement(True)
        else:
            element.setDefaultElement(False)
        element.setAlgorithm(svars.get(self._prefix + 'algorithm'))
        
    def saveElement(self, element):
        entityManager.persist(element)
        entityManager.flush()
        
    def findElementById(self, id):
        return entityManager.createQuery('Select element From Element element Where element.id = ' + str(id)).getSingleResult()
        
    def findSubElementCommunity(self, id):
        return entityManager.createQuery('Select element From ElementCommunity element Where element.id = ' + str(id)).getSingleResult()
        
    def findSubElementPossession(self, id):
        return entityManager.createQuery('Select element From ElementPossession element Where element.id = ' + str(id)).getSingleResult()
    
    def findCommunityElement(self, elementId, communityId):
        try:
            return entityManager.createQuery('Select element From ElementCommunity element join element.element parent join element.community community Where parent.id = %s and community.id = %s' % (str(elementId), str(communityId))).getSingleResult()
        except:
            self._logger.info('Community(%s) element(%s) not found' % (communityId, elementId))
            return None
    
    def findPossessionElement(self, elementId, possessionId):
        try:
            return entityManager.createQuery('Select element From ElementPossession element join element.element parent join element.possession possession Where parent.id = %s and possession.id = %s' % (str(elementId), str(possessionId))).getSingleResult()
        except:
            return None
    
    def findGroupById(self, id):
        return entityManager.createQuery('Select dict From Dictionary dict Where dict.id = ' + str(id)).getSingleResult()
    
    def findDefaultElements(self):
        return entityManager.createQuery('Select element From Element element where element.defaultElement = 1').getResultList()