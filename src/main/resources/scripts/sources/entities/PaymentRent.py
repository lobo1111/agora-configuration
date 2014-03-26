from pl.reaper.container.data import PaymentRent
from pl.reaper.container.data import PaymentRentDetails
from java.text import SimpleDateFormat

class PaymentRentManager(Container):
    
    def create(self):
        paymentRent = PaymentRent()
        self.setPaymentRentData(paymentRent)
        self.savePaymentRent(paymentRent)
        
    def remove(self):
        global svars
        paymentRent = self.findPaymentRentById(svars.get('id'))
        currentMonth = self.getCurrentMonth()
        currentBookingPeriod = self.getBookingPeriod()
        if paymentRent.getMonth() == currentMonth and paymentRent.getBookingPeriod().getId() == currentBookingPeriod.getId():
            entityManager.remove(paymentRent.getPaymentRentDetails())
            entityManager.remove(paymentRent)
            entityManager.flush()
            
    def removeCharging(self):
        global svars
        charging = self.findChargingById(svars.get('id'))
        currentMonth = self.getCurrentMonth()
        currentBookingPeriod = self.getBookingPeriod()
        if charging.getMonth() == currentMonth and charging.getBookingPeriod().getId() == currentBookingPeriod.getId():
            for element in charging.getChargingElements():
                entityManager.remove(element)
            charging.getChargingElements().clear()
            entityManager.remove(charging)
            entityManager.flush()
        
        
    def setPaymentRentData(self, paymentRent):
        global svars
        paymentRentDetails = PaymentRentDetails()
        paymentRentDetails.setPaymentRent(paymentRent)
        paymentRent.setPaymentRentDetails(paymentRentDetails)
        paymentRent.setPossession(self.getPossession())
        paymentRent.setMonth(self.getCurrentMonth())
        paymentRent.setBookingPeriod(self.getBookingPeriod())
        paymentRentDetails.setTitle(svars.get('title'))
        paymentRentDetails.setBookingDate(self.parseDate(svars.get('bookingDate')))
        paymentRentDetails.setRequestDate(self.parseDate(svars.get('requestDate')))
        paymentRentDetails.setClientName(svars.get('clientName'))
        paymentRentDetails.setAccount(self.getAccount())
        paymentRentDetails.setValue(float(svars.get('value')))
        paymentRentDetails.setAuto(False)
    
    def savePaymentRent(self, paymentRent):
        entityManager.persist(paymentRent)
        entityManager.flush()

    def getPossession(self):
        global svars
        possessionId = int(svars.get('possessionId'))
        return entityManager.createQuery('Select p From Possession p Where p.id = %d' % possessionId).getSingleResult()
    
    def getAccount(self):
        global svars
        accountId = int(svars.get('accountId'))
        return entityManager.createQuery('Select a From Account a Where a.id = %d' % accountId).getSingleResult()
    
    def getCurrentMonth(self):
        return entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
    
    def getBookingPeriod(self):
        return entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    
    def parseDate(self, dateAsString):
        try:
            return SimpleDateFormat('dd-MM-yy').parse(dateAsString)
        except:
            return None
        
    def findPaymentRentById(self, id):
        return entityManager.createQuery('Select p From PaymentRent p Where p.id = %d' % int(id)).getSingleResult()
    
    def findChargingById(self, id):
        return entityManager.createQuery('Select p From Charging p Where p.id = %d' % int(id)).getSingleResult()