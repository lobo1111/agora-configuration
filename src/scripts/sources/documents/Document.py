from java.util import Date
from java.math import BigDecimal
from java.math import RoundingMode
from base.Container import Container
from structures.BookingPeriod import BookingPeriodManager
from pl.reaper.container.data import Document
from pl.reaper.container.data import DocumentPosition

class DocumentManager(Container):
    
    def initDocument(self, type):
        document = Document()
        document.setCreatedAt(Date())
        document.setType(type)
        document.setCommunity(self.findById("Community", int(self._svars.get('communityId'))))
        if self._svars.get('possessionId') != None and self._svars.get('possessionId') != '0':
            document.setPossession(self.findById("Possession", int(self._svars.get('possessionId'))))
        if self._svars.get('contractorId') != None and self._svars.get('contractorId') != '0':
            document.setContractor(self.findById("Contractor", int(self._svars.get('contractorId'))))
        document.setDescription(self._svars.get('documentDescription'))
        self._logger.info("New document of type %s created" % document.getType())
        return document
        
    def initPosition(self, document, prefix = ''):
        position = DocumentPosition()
        position.setCreatedAt(Date())
        position.setType(document.getType() + "_POSITION")
        position.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
        position.setMonth(BookingPeriodManager().getCurrentMonth().getValue())
        value = self.parseFloat(self._svars.get(prefix + 'value'))
        position.setValue(BigDecimal(value).setScale(2, RoundingMode.HALF_UP))
        position.setDescription(self._svars.get(prefix + 'positionDescription'))
        if self._svars.get(prefix + 'accountId') != None and int(self._svars.get(prefix + 'accountId')) > 0:
            position.setAccount(self.findById("Account", int(self._svars.get(prefix + 'accountId'))))
        else:
            self._logger.info("Position doesn't have accountID set under key %s" % (prefix + 'accountId'))
        self._logger.info("New document position of type %s created(%f)" % (position.getType(), position.getValue().floatValue()))
        return position
    
    def bound(self, document, position):
        if not position in document.getPositions():
            document.getPositions().add(position)
            position.setDocument(document)
            self._logger.info("Document %s bound with %s position" % (document.getType(), position.getType()))
    
    def save(self, entity):
        self.saveEntity(entity)
        return entity

    def saveDocument(self, document):
        self._logger.info("Saving document %s with %d position(s)" % (document.getType(), document.getPositions().size()))
        return self.save(document)

    def savePosition(self, position):
        return self.save(position)
        
    def closeDocument(self, document):
        if self.isEditable(document) and self.positionsAreBooked(document.getPositions()):
            document.setClosed(True)
            document.setClosedAt(Date())
            self.saveDocument(document)
            self._logger.info("Document %d closed" % document.getId())
        else:
            self._logger.info("Document %d can't be closed" % document.getId())
            
    def cancelDocument(self, document):
        if self.isEditable(document) and not self.positionsAreBooked(document.getPositions()):
            self.cancelPositions(document.getPositions())
            document.setCanceled(True)
            document.setCanceledAt(Date())
            self.saveDocument(document)
            self._logger.info("Document %d canceled" % document.getId())
        else:
            self._logger.info("Document %d can't be canceled" % document.getId())
            
    def isEditable(self, document):
        return (not document.isClosed() and not document.isCanceled())
    
    def positionsAreBooked(self, positions):
        for position in positions:
            if not position.isBooked():
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
            debitBalance = position.getDebitZpk().getCurrentBalance()
            creditBalance = position.getCreditZpk().getCurrentBalance()
            debitBalance.setDebit(position.getValue().add(BigDecimal(debitBalance.getDebit())).floatValue())
            creditBalance.setCredit(position.getValue().add(BigDecimal(creditBalance.getCredit())).floatValue())
            position.setBooked(True)
            position.setBookedAt(Date())
            self.saveEntity(debitBalance)
            self.saveEntity(creditBalance)
            self.savePosition(position)
            
    def cancelPosition(self, position):
        if not position.isBooked() and not position.isCanceled():
            position.setCanceled(True)
            position.setCanceledAt(Date())
            self.savePosition(position)
            self._logger.info("Document position %d canceled" % position.getId())
        else:
            self._logger.info("Document position %d can't be canceled" % position.getId())
            
    def bookDocument(self, document):
        if self.isEditable(document):
            self.bookPositions(document.getPositions())
            self.saveDocument(document)
        
    def bookAll(self):
        currentMonth = BookingPeriodManager().getCurrentMonth().getValue()
        currentBookingPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        sql = "Select distinct document From Document document join document.positions p Where p.month = '%s' and p.bookingPeriod.id = %d" % (currentMonth, currentBookingPeriod.getId())
        for document in self._entityManager.createQuery(sql).getResultList():
            self.bookDocument(document)
        
    def findZpk(self, zpks, typeKey):
        zpkType = self.findDictionary(str(self.findZpkSettingId(typeKey)))
        matched = [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()]
        if len(matched) == 1:
            return matched[0]
        else:
            self._logger.info("ZPK of type %s not found in:" % typeKey)
            for zpk in zpks:
                self._logger.info("%s - %s" % (zpk.getNumber(), zpk.getType().getKey()))
            
    def findDictionary(self, id):
        return self._entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        self._logger.info('Looking for ZPK of type %s' % str(typeKey))
        return self._entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()
        
