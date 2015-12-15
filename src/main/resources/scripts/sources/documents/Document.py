from java.util import Date
from java.math import BigDecimal
from base.Container import Container
from entities.BookingPeriod import BookingPeriodManager
from pl.reaper.container.data import Document
from pl.reaper.container.data import DocumentPosition

class DocumentManager(Container):
    
    def initDocument(self, type):
        document = Document()
        document.setCreatedAt(Date())
        document.setType(type)
        document.setCommunity(self.findById("Community", int(self._svars.get('communityId'))))
        if self._svars.get('possessionId') != None:
            document.setPossession(self.findById("Possession", int(self._svars.get('possessionId'))))
        if self._svars.get('contractorId') != None:
            document.setContractor(self.findById("Contractor", int(self._svars.get('contractorId'))))
        document.setDescription(self._svars.get('documentDescription'))
        return document
        
    def initPosition(self, document, prefix = ''):
        position = DocumentPosition()
        position.setCreatedAt(Date())
        position.setType(document.getType() + "_POSITION")
        document.getPositions().add(position)
        position.setDocument(document)
        position.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
        position.setMonth(BookingPeriodManager().getCurrentMonth())
        position.setValue(BigDecimal(self._svars.get(prefix + 'value')))
        position.setDescription(self._svars.get(prefix + 'positionDescription'))
        return position

    def saveDocument(self, document):
        self.saveEntity(document)
        return document

    def savePosition(self, position):
        self.saveEntity(position)
        return position
        
    def closeDocument(self, document):
        if self.isEditable(document) and self.positionsAreBooked(document.getPositions()):
            document.setClosed(True)
            document.setClosedAt(Date())
            self.saveDocument(document)
            
    def cancelDocument(self, document):
        if self.isEditable(document) and not self.positionsAreBooked(document.getPositions()):
            self.cancelChildren(document.getPositions())
            self.setCanceled(True)
            self.setCanceledAt(Date())
            self.saveDocument(document)
            
    def isEditable(self, document):
        return (not document.isClosed() and not document.isCanceled())
    
    def positionsAreBooked(self, positions):
        for position in positions:
            if not position.isBooked() and not position.isCanceled():
                return False
        return True
    
    def cancelPositions(self, positions):
        for position in positions:
            self.cancelPosition(position)
            
    def bookPositions(self, positions):
        for position in positions:
            self.bookPosition(position)
            
    def bookPosition(self, position):
        if not position.isCanceled() and not position.isBooked() and position.getCreditZpk() != None and position.getDebitZpk() != None:
            position.setDebit(position.getDebit() + position.getValue())
            position.setCredit(position.getCredit() + position.getValue())
            position.setBooked(True)
            position.setBookedAt(Date())
            self.savePosition(position)
            
    def cancelPosition(self, position):
        if not position.isBooked() and not positions.isCanceled():
            position.setCanceled(True)
            self.savePosition(position)
            
    def bookDocument(self, document):
        if self.isEditable(document):
            self.bookPositions(document.getPositions())
            self.saveDocument(document)
        
    def bookAllPositions(self):
        currentMonth = BookingPeriodManager().getCurrentMonth()
        currentBookingPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        sql = "Select document From Document document Where document.month = '%s' and document.bookingPeriod.id = %d" % (currentMonth, currentBookingPeriod.getId())
        for document in self._entityManager.createQuery(sql).getResultList():
            self.bookDocument(document)
            
    def findZpk(self, zpks, typeKey):
        zpkType = self.findDictionary(str(self.findZpkSettingId(typeKey)))
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()][0]
            
    def findDictionary(self, id):
        return self._entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return self._entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()
            

                
            