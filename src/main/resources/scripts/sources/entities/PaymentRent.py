from pl.reaper.container.data import PaymentRent
from pl.reaper.container.data import PaymentRentDetails
from java.text import SimpleDateFormat
from base.Container import Container
from entities.InternalPayment import InternalPaymentManager

class PaymentRentManager(Container):
    
    def create(self):
        paymentRent = PaymentRent()
        self.setPaymentRentData(paymentRent)
        self.savePaymentRent(paymentRent)
        
    def remove(self):
        paymentRent = self.findPaymentRentById(self._svars.get('id'))
        currentBookingPeriod = self.getBookingPeriod()
        if paymentRent.getBookingPeriod().getId() == currentBookingPeriod.getId() and paymentRent.getInternalPayment() != None:
            internalPayment = paymentRent.getInternalPayment()
            InternalPaymentManager().cancelBookedPayment(internalPayment)
        self._entityManager.remove(paymentRent.getPaymentRentDetails())
        self._entityManager.remove(paymentRent)
        self._entityManager.flush()
            
    def removeCharging(self):
        charging = self.findChargingById(self._svars.get('id'))
        currentMonth = self.getCurrentMonth()
        currentBookingPeriod = self.getBookingPeriod()
        if charging.getBookingPeriod().getId() == currentBookingPeriod.getId() and charging.getInternalPayment() != None:
            internalPayment = charging.getInternalPayment()
            InternalPaymentManager().cancelBookedPayment(internalPayment)
        for element in charging.getChargingElements():
            self._entityManager.remove(element)
        charging.getChargingElements().clear()
        self._entityManager.remove(charging)
        self._entityManager.flush()
        
        
    def setPaymentRentData(self, paymentRent):
        paymentRentDetails = PaymentRentDetails()
        paymentRentDetails.setPaymentRent(paymentRent)
        paymentRent.setPaymentRentDetails(paymentRentDetails)
        paymentRent.setPossession(self.getPossession())
        paymentRent.setMonth(self.getCurrentMonth())
        paymentRent.setBookingPeriod(self.getBookingPeriod())
        paymentRentDetails.setTitle(self._svars.get('title'))
        paymentRentDetails.setBookingDate(self.parseDate(self._svars.get('bookingDate')))
        paymentRentDetails.setRequestDate(self.parseDate(self._svars.get('requestDate')))
        paymentRentDetails.setClientName(self._svars.get('clientName'))
        paymentRentDetails.setAccount(self.getAccount())
        paymentRentDetails.setValue(float(self._svars.get('value')))
        paymentRentDetails.setAuto(False)
    
    def savePaymentRent(self, paymentRent):
        self._entityManager.persist(paymentRent)
        self._entityManager.flush()

    def getPossession(self):
        
        possessionId = int(self._svars.get('possessionId'))
        return self._entityManager.createQuery('Select p From Possession p Where p.id = %d' % possessionId).getSingleResult()
    
    def getAccount(self):
        
        accountId = int(self._svars.get('accountId'))
        return self._entityManager.createQuery('Select a From Account a Where a.id = %d' % accountId).getSingleResult()
    
    def getCurrentMonth(self):
        return self._entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
    
    def getBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    
    def parseDate(self, dateAsString):
        try:
            return SimpleDateFormat('dd-MM-yyyy').parse(dateAsString)
        except:
            return None
        
    def findPaymentRentById(self, id):
        return self._entityManager.createQuery('Select p From PaymentRent p Where p.id = %d' % int(id)).getSingleResult()
    
    def findChargingById(self, id):
        return self._entityManager.createQuery('Select p From Charging p Where p.id = %d' % int(id)).getSingleResult()