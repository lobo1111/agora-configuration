from base.Container import Container
from entities.InternalPayment import InternalPaymentManager

class BankNoteBooker(Container):
    
    def bookAllNotes(self):
        self._logger.info("Bank Note Booker starts...")
        [self.bookNote(note) for note in self.collectNotes()]
        self._logger.info("All bank notes booked")
        
    def collectNotes(self):
        return self._entityManager.createQuery('Select c From BankNote c Where c.internalPayment is null').getResultList()
    
    def bookNote(self, note):
        self._logger.info("Booking note %d" % note.getId())
        zpkCredit, zpkDebit = self.collectZpks(note)
        self.createAndBookPayment(note, zpkCredit, zpkDebit)

    def createAndBookPayment(self, note, zpkCredit, zpkDebit):
        self._svars.put('creditZpkId', str(zpkCredit.getId()))
        self._svars.put('debitZpkId', str(zpkDebit.getId()))
        self._svars.put('amount', str(note.getNoteValue()))
        self._svars.put('comment', 'Nota')
        manager = InternalPaymentManager()
        payment = manager.create()
        note.setInternalPayment(payment)
        self.saveEntity(payment)
        self._entityManager.flush()
        self._svars.put('paymentId', str(payment.getId()))
        manager.book()

    def collectZpks(self, note):
        zpkCredit = self.findRentCreditZpk(note.getPossession().getCommunity())
        zpkDebit = self.getZpkRent(note.getPossession().getZpks())
        return zpkCredit, zpkDebit

    def getZpkRent(self, zpks):
        return self.findZpk(zpks, 'POSSESSION')
    
    def findRentCreditZpk(self, community):
        return self.findZpk(community.getZpks(), 'CHARGING_RENT')
    
    def findZpk(self, zpks, typeKey):
        zpkType = self.findZpkType(typeKey)
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()][0]
            
    def findZpkType(self, typeKey):
        return self.findDictionary(str(self.findZpkSettingId(typeKey)))
    
    def findDictionary(self, id):
        return self._entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return self._entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()