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
        element = self.findElementById(self._svars.get(self._prefix + 'id'))
        self.setElementData(element)
        self.saveElement(element)
        return element
    
    def multiUpdate(self):
        for i in range(int(self._svars.get(self._prefix + 'counter'))):
            newValueAsString = self._svars.get(str(i) + '_newValue')
            communityElementId = self._svars.get(str(i) + '_id')
            if newValueAsString != '':
                newValue = float(newValueAsString)
                communityElement = self.findCommunityElementById(communityElementId)
                communityElement.setGlobalValue(newValue)
                self._entityManager.persist(communityElement)
        self._entityManager.flush()
            
        
    def CreateOrUpdateCommunityElement(self, community):
        elementId = self._svars.get("elementId")
        communityId = community.getId()
        communityElement = self.findCommunityElement(elementId, communityId)
        createElementForPossessions = False
        if communityElement is None:
            communityElement = ElementCommunity()
            createElementForPossessions = True
            communityElement.setElement(self.findElementById(elementId))
            communityElement.setCommunity(community)
            community.getElements().add(communityElement)
        if self._svars.get('override') == 'true':
            communityElement.setOverrideParentValue(True)
        else:
            communityElement.setOverrideParentValue(False)
        if not self._svars.get("overrideValue") is None and not self._svars.get("overrideValue") == '':
            communityElement.setGlobalValue(float(self._svars.get("overrideValue")))
        if createElementForPossessions:
            tmpOverride = self._svars.get('override')
            tmpOverrideValue = self._svars.get("overrideValue")
            self.setElementForPossessions(community, communityElement)
            self._svars.put('override', tmpOverride)
            self._svars.put('overrideValue', tmpOverrideValue)
        self._entityManager.persist(communityElement)
        self._entityManager.flush()
        return communityElement
        
    def setElementForPossessions(self, community, communityElement):
        for possession in community.getPossessions():
            self._svars.put("overrideValue", "0")
            self._svars.put("override", "false")
            self.CreateOrUpdatePossessionElement(possession, communityElement, False)
            
    def propagateElementsForNewPossession(self, possession):
        for communityElement in possession.getCommunity().getElements():
            self._logger.info('Propagating element for new possession - %d' % communityElement.getElement().getId())
            self._svars.put("elementId", str(communityElement.getElement().getId()))
            self.CreateOrUpdatePossessionElement(possession, communityElement, False)
            
    def CreateOrUpdatePossessionElement(self, possession, elementCommunity = None, override = True):
        elementId = self._svars.get("elementId")
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
            if self._svars.get('override') == 'true':
                possessionElement.setOverrideParentValue(True)
            else:
                possessionElement.setOverrideParentValue(False)
            possessionElement.setGlobalValue(float(self._svars.get('overrideValue')))
        self._entityManager.persist(possession)
        self.saveElement(possessionElement)
        return possessionElement

    def dropCommunityElement(self, communityElementId):
        communityElement = self.findById('ElementCommunity', communityElementId)
        for possessionElement in communityElement.getPossessionsElements():
            self.dropPossessionElement(possessionElement.getId())
        communityElement.getCommunity().getElements().remove(communityElement)
        self._entityManager.remove(communityElement)
        self._entityManager.persist(communityElement.getCommunity())

    def dropPossessionElement(self, possessionElementId):
        possessionElement = self.findById('ElementPossession', possessionElementId)
        possessionElement.getPossession().getElements().remove(possessionElement)
        self._entityManager.remove(possessionElement)
        self._entityManager.persist(possessionElement.getPossession())
            
    def setElementData(self, element):
        element.setName(self._svars.get(self._prefix + 'name'))
        element.setKey(self._svars.get(self._prefix + 'key'))
        element.setGlobalValue(BigDecimal(self._svars.get(self._prefix + 'value')).floatValue())
        element.setGroup(self.findGroupById(self._svars.get(self._prefix + 'groupId')))
        if self._svars.get(self._prefix + 'defaultValue') == 'true':
            element.setDefaultElement(True)
        else:
            element.setDefaultElement(False)
        element.setAlgorithm(self.findById('PaymentAlgorithm', int(self._svars.get(self._prefix + 'algorithm'))))
        
    def saveElement(self, element):
        self.saveEntity(element)
        
    def findElementById(self, id):
        return self._entityManager.createQuery('Select element From Element element Where element.id = ' + str(id)).getSingleResult()
        
    def findCommunityElementById(self, id):
        return self._entityManager.createQuery('Select element From ElementCommunity element Where element.id = ' + str(id)).getSingleResult()
        
    def findSubElementCommunity(self, id):
        return self._entityManager.createQuery('Select element From ElementCommunity element Where element.id = ' + str(id)).getSingleResult()
        
    def findSubElementPossession(self, id):
        return self._entityManager.createQuery('Select element From ElementPossession element Where element.id = ' + str(id)).getSingleResult()
    
    def findCommunityElement(self, elementId, communityId):
        try:
            return self._entityManager.createQuery('Select element From ElementCommunity element join element.element parent join element.community community Where parent.id = %s and community.id = %s' % (str(elementId), str(communityId))).getSingleResult()
        except:
            self._logger.info('Community(%s) element(%s) not found' % (communityId, elementId))
            return None
    
    def findPossessionElement(self, elementId, possessionId):
        try:
            return self._entityManager.createQuery('Select element From ElementPossession element join element.element parent join element.possession possession Where parent.id = %s and possession.id = %s' % (str(elementId), str(possessionId))).getSingleResult()
        except:
            return None
    
    def findGroupById(self, id):
        return self._entityManager.createQuery('Select dict From Dictionary dict Where dict.id = ' + str(id)).getSingleResult()
    
    def findDefaultElements(self):
        return self._entityManager.createQuery('Select element From Element element where element.defaultElement = 1').getResultList()