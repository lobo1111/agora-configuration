from pl.reaper.container.data import PaymentRent
from pl.reaper.container.data import PaymentRentDetails
from java.text import SimpleDateFormat

class PaymentRentManager(Container):
    
    def create(self):
        paymentRent = PaymentRent()
        self.setPaymentRentData(paymentRent)
        self.savePaymentRent(paymentRent)
        
    def remove(self):
        paymentRent = self.findPaymentRentById(vars.get('id'))
        currentMonth = self.getCurrentMonth()
        currentBookingPeriod = self.getCurrentBookingPeriod()
        if paymentRent.getMonth() == currentMonth and paymentRent.getCurrentBookingPeriod().getId() == currentBookingPeriod.getId():
            entityManager.remove(paymentRent)
            entityManager.flush()
            
    def removeCharging(self):
        charging = self.findChargingById(vars.get('id'))
        currentMonth = self.getCurrentMonth()
        currentBookingPeriod = self.getCurrentBookingPeriod()
        if charging.getMonth() == currentMonth and charging.getCurrentBookingPeriod().getId() == currentBookingPeriod.getId():
            entityManager.remove(charging)
            entityManager.flush()
        
        
    def setPaymentRentData(self, paymentRent):
        paymentRentDetails = PaymentRentDetails()
        paymentRentDetails.setPaymentRent(paymentRent)
        paymentRent.setPaymentRentDetails(paymentRentDetails)
        paymentRent.setPossession(self.getPossession())
        paymentRent.setMonth(self.getCurrentMonth())
        paymentRent.setBookingPeriod(self.getBookingPeriod())
        paymentRentDetails.setTitle(vars.get('title'))
        paymentRentDetails.setBookingDate(self.parseDate(vars.get('bookingDate')))
        paymentRentDetails.setRequestDate(self.parseDate(vars.get('requestDate')))
        paymentRentDetails.setClientName(vars.get('clientName'))
        paymentRentDetails.setAccount(self.getAccount())
        paymentRentDetails.setValue(float(vars.get('value')))
        paymentRentDetails.setAuto(False)
    
    def savePaymentRent(self, paymentRent):
        entityManager.persist(paymentRent)
        entityManager.flush()

    def getPossession(self):
        possessionId = int(vars.get('possessionId'))
        return entityManager.createQuery('Select p From Possession p Where p.id = %d' % possessionId).getSingleResult()
    
    def getAccount(self):
        accountId = int(vars.get('accountId'))
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
        return entityManager.createQuery('Select p From PaymentRent p Where p.id = %d' % int(id))
    
    def findChargingById(self, id):
        return entityManager.createQuery('Select p From Charging p Where p.id = %d' % int(id))