from base.Container import Container
from java.math import BigDecimal
from documents.Document import DocumentManager
from pl.reaper.container.data import Document
from pl.reaper.container.data import DocumentPosition
from entities.BookingPeriod import BookingPeriodManager

class PaymentRentMigrator(Container):
    
    def migrateAll(self):
        for pr in self.collect():
            if not self.alreadyMigrated(pr.getId()):
                self._logger.info('Migrating payment rent %d...' % pr.getId())
                document = Document()
                document.setType('POSSESSION_PAYMENT')
                document.setCommunity(pr.getPossession().getCommunity())
                document.setPossession(pr.getPossession())
                document.setCreatedAt(pr.getTimestamp())
                document.setDescription(pr.getComment())
                document.putAttribute('MIGRATED', str(pr.getId()))
                documentPosition = DocumentPosition()
                documentPosition.setType('POSSESSION_PAYMENT_POSITION')
                documentPosition.setCreatedAt(pr.getTimestamp())
                documentPosition.setValue(BigDecimal(pr.getPaymentRentDetails().getValue()))
                documentPosition.setMonth(pr.getMonth())
                if pr.getInternalPayment() != None:
                    documentPosition.setBookingPeriod(pr.getInternalPayment().getBookingPeriod())
                    documentPosition.setBooked(True)
                else:
                    documentPosition.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
                    documentPosition.setBooked(False)
                documentPosition.setDescription(pr.getPaymentRentDetails().getTitle())
                documentPosition.setClientName(pr.getPaymentRentDetails().getClientName())
                documentPosition.setAccount(pr.getPaymentRentDetails().getAccount())
                documentPosition.putAttribute('CREATE_DATE', pr.getPaymentRentDetails().getRequestDate())
                documentPosition.putAttribute('BOOKING_DATE', pr.getPaymentRentDetails().getBookingDate())
                if pr.isRepairFund():
                    paymentPosition.setCreditZpk(self.findZpk(pr.getPossession().getZpks(), 'POSSESSION_REPAIR_FUND'))
                    paymentPosition.setDebitZpk(self.findZpk(pr.getPaymentRentDetails().getAccount().getZpks(), 'REPAIR_FUND'))
                else:
                    paymentPosition.setCreditZpk(self.findZpk(pr.getPossession().getZpks(), 'POSSESSION'))
                    paymentPosition.setDebitZpk(self.findZpk(pr.getPaymentRentDetails().getAccount().getZpks(), 'RENT', 'DEFAULT'))
                DocumentManager().bound(document, documentPosition)
                self.saveEntity(document)
            else:
                self._logger.info('Payment rent %d already migrated, skipping...' % pr.getId())
            
    def collect(self):
        sql = "Select i From PaymentRent i"
        return self._entityManager.createQuery(sql).getResultList()
    
    def alreadyMigrated(self, id):
        sql = "Select count(a) From Document d Join d.attributes a Where d.type = 'POSSESSION_PAYMENT' And a.name = 'MIGRATED' And a.value = %s" % str(id)
        return self._entityManager.createQuery(sql).getSingleResult() > 0
    
    def findZpk(self, zpks, typeKey, alternative = ''):
        zpkType = DocumentManager().findDictionary(str(DocumentManager().findZpkSettingId(typeKey)))
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey() or zpk.getType().getKey() == alternative][0]