from pl.reaper.container.data import Charging
from pl.reaper.container.data import ChargingElement
from base.Container import Container
from entities.ChargingQueue import ChargingQueueManager
from java.util import Date
import re

class Calculator(Container):
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
                self._logger.info('Entity not found, assuming attribute value = 0')
                value = 0
            else:
                try:
                    value = self.getAttributeValue(instance, attribute)
                    self._logger.info('Value established = ' + str(value))
                except:
                    value = 0
                    self._logger.info('Exception raised, attribute not found(%s). Assuming attribute value = 0' % attribute)
            algorithm = algorithm.replace('#{' + entity + '.' + attribute + '}', str(value))
        algorithmValue = eval(algorithm)
        print str(algorithm) + '=' + str(algorithmValue)
        return algorithmValue

class ChargeManager(Container):
    
    def chargeAll(self):
        self._logger.info('Processing charge requests...')
        self._queue = ChargingQueueManager()
        self._queue.setEntityManager(self._entityManager)
        self._queue.setSvars(self._svars)
        self._currentMonth = self.getCurrentMonth()
        self._logger.info('Charging month: %s' % str(self._currentMonth))
        self._bookingPeriod = self.getBookingPeriod()
        item = self._queue.popFromQueue()
        while not item is None:
            self._logger.info('charging: %s' % item.getType())
            self.charge(item)
            item = self._queue.popFromQueue()
        self._logger.info('All charge request processed.')
            
    def alreadyCharged(self, possession):
        try:
            self._entityManager.createQuery("Select p From Charging c Join c.possession p Where p.id = " + str(possession.getId()) + " and c.month = %s)" % self._currentMonth).getSingleResult()
            return True
        except:
            return False
    
    def charge(self, item):
        if item.getType().toString() == "ALL":
            self.chargeAllUncharged()
        elif item.getType().toString() == "COMMUNITY":
            self.chargeCommunity(item.getCommunity())
        elif item.getType().toString() == "POSSESSION":
            self.chargePossession(item.getPossession())
            
    def chargePossession(self, possession, check = True):
        if (not check) or (not self.alreadyCharged(possession)):
            charging = Charging()
            charging.setPossession(possession)
            charging.setBookingPeriod(self._bookingPeriod)
            charging.setMonth(self._currentMonth)
            charging.setTimestamp(Date())
            for possessionElement in possession.getElements():
                charging.getChargingElements().add(self.calculate(charging, possession, possessionElement))
            if charging.getChargingElements().size() > 0:
                self._entityManager.persist(charging)
        else:
            self._logger.info('Looks like possession %s is already charged, omitting...' % str(possession.getId()))
    
    def chargeCommunity(self, community):
        for possession in community.getPossessions():
            self.chargePossession(possession)
            
    def chargeAllUncharged(self):
        for possession in self.findAllUncharged():
            self._logger.info('Charging possession %s' % str(possession.getId()))
            self.chargePossession(possession, False)
            
    def getBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    
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
        elif possessionElement.getElementCommunity() != None and possessionElement.getElementCommunity().isOverrideParentValue():
            return possessionElement.getElementCommunity().getGlobalValue()
        else:
            return possessionElement.getElement().getGlobalValue()
            
    def findAllUncharged(self):
        return self._entityManager.createQuery("Select p From Possession p Where p.id not in(Select ped.id From Charging c Join c.bookingPeriod bp Join c.possession ped Where bp.defaultPeriod = 1 AND c.month = %s)" % self._currentMonth).getResultList()
            
    def getCurrentMonth(self):
        return self._entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()