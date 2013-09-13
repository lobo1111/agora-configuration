from pl.reaper.container.data import Charging
from pl.reaper.container.data import ChargingElement

import re

class Calculator:
    def capitalize(self, line):
        return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])
    
    def getAttributeValue(self, instance, attribute):
        result = getattr(instance, 'get' + self.capitalize(attribute))()
        if hasattr(result, 'floatValue'):
            return getattr(result, 'floatValue')()
        else:
            return result
    
    def calculate(self, element, possession):
        entities = {"element" : element, "possession" : possession}
        if possession is not None:
            entities['possessionData'] = possession.getAdditionalData()
        algorithm = element.getAlgorithm()
        occurences = re.findall('#\{(.+?)\.(.+?)\}', algorithm)
        for occurence in occurences:
            entity = occurence[0]
            attribute = occurence[1]
            print 'Looking for %s.%s' % (entity, attribute)
            instance = entities.get(entity)
            if instance is None:
                print 'Entity not found, assuming attribute value = 0'
                value = 0
            else:
                try:
                    value = self.getAttributeValue(instance, attribute)
                    print 'Value established = ' + str(value)
                except:
                    value = 0
                    print 'Exception raised, attribute not found(%s). Assuming attribute value = 0' % attribute
            algorithm = algorithm.replace('#{' + entity + '.' + attribute + '}', str(value))
        algorithmValue = eval(algorithm)
        print str(algorithm) + '=' + str(algorithmValue)
        return algorithmValue

class ChargeManager:
    _logger = Logger([:_scriptId])
    
    def chargeAll(self):
        self._logger.info('Processing charge requests...')
        self._queue = ChargingQueueManager()
        self._currentMonth = self.getCurrentMonth()
        self._bookingPeriod = self.getBookingPeriod()
        item = self._queue.popFromQueue()
        while not item is None:
            self._logger.info('charging: %s' % item.getType())
            self.charge(item)
            item = self._queue.popFromQueue()
        self._logger.info('All charge request processed.')
            
    def alreadyCharged(self, possession):
        try:
            entityManager.createQuery("Select p From Charging c Join c.possession p Where p.id = " + str(possession.getId())).getSingleResult()
            return True
        except:
            return False
    
    def charge(self, item):
        if item.getType().toString() == "ALL":
            self.chargeAllCommunities()
        elif item.getType().toString() == "COMMUNITY":
            self.chargeCommunity(item.getCommunity())
        elif item.getType().toString() == "POSSESSION":
            self.chargePossession(item.getPossession())
            
    def chargePossession(self, possession):
        if not self.alreadyCharged(possession):
            charging = Charging()
            charging.setPossession(possession)
            charging.setBookingPeriod(self._bookingPeriod)
            charging.setMonth(self._currentMonth)
            for possessionElement in possession.getElements():
                charging.getChargingElements().add(self.calculate(charging, possession, possessionElement))
            entityManager.persist(charging)
    
    def chargeCommunity(self, community):
        for possession in community.getPossessions():
            self.chargePossession(possession)
            
    def chargeAllCommunities(self):
        for community in self.findAllCommunities():
            self.chargeCommunity(community)
            
    def getBookingPeriod(self):
        return entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    
    def calculate(self, charging, possession, possessionElement):
        element = possessionElement.getElement()
        element.setGlobalValue(self.discoverValue(possessionElement))
        calculator = Calculator()
        cElement = ChargingElement()
        cElement.setKey(element.getKey())
        cElement.setName(element.getName())
        cElement.setGroup(element.getGroup())
        cElement.setValue(calculator.calculate(element, possession))
        cElement.setCharging(charging)
        return cElement
    
    def discoverValue(self, possessionElement):
        if possessionElement.isOverrideParentValue():
            return possessionElement.getGlobalValue()
        elif possessionElement.getElementCommunity().isOverrideParentValue():
            return possessionElement.getElementCommunity().getGlobalValue()
        else:
            return possessionElement.getElement().getGlobalValue()
            
    def findAllCommunities(self):
        return entityManager.createQuery("Select c From Community c").getResultList()
            
    def getCurrentMonth(self):
        return entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()