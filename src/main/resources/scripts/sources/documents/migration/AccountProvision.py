from base.Container import Container
from java.math import BigDecimal
from documents.Document import DocumentManager
from pl.reaper.container.data import Document
from pl.reaper.container.data import DocumentPosition
from entities.BookingPeriod import BookingPeriodManager

class AccountProvisionMigrator(Container):
    
    def migrateAll(self):
        for ap in self.collect():
            if not self.alreadyMigrated(ap.getId()):
                self._logger.info('Migrating account provision %d...' % ap.getId())
                document = Document()
                document.setType('ACCOUNT_PROVISION')
                document.setCommunity(ap.getAccount().getCommunity())
                document.setCreatedAt(ap.getCreatedAt())
                document.putAttribute('CREATE_DATE', str(ap.getId()))
                document.putAttribute('MIGRATED', str(ap.getId()))
                documentPosition = DocumentPosition()
                documentPosition.setAccount(ap.getAccount())
                documentPosition.setType('ACCOUNT_PROVISION_POSITION')
                documentPosition.setCreatedAt(ap.getCreatedAt())
                documentPosition.setValue(BigDecimal(ap.getProvisionValue()))
                if ap.getInternalPayment() != None:
                    documentPosition.setBookingPeriod(ap.getInternalPayment().getBookingPeriod())
                    documentPosition.setMonth(ap.getMonth())
                    documentPosition.setBooked(True)
                else:
                    documentPosition.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
                    documentPosition.setMonth('0')
                    documentPosition.setBooked(False)
                documentPosition.setCreditZpk(DocumentManager().findZpk(ap.getAccount().getCommunity().getZpks(), 'RENT'))
                documentPosition.setDebitZpk(DocumentManager().findZpk(ap.getAccount().getBankContractor().getZpks(), 'CONTRACTOR'))
                DocumentManager().bound(document, documentPosition)
                self.saveEntity(document)
            else:
                self._logger.info('Note %d already migrated, skipping...' % note.getId())
            
    def collect(self):
        sql = "Select i From AccountProvision i"
        return self._entityManager.createQuery(sql).getResultList()
    
    def alreadyMigrated(self, id):
        sql = "Select count(a) From Document d Join d.attributes a Where d.type = 'ACCOUNT_PROVISION' And a.name = 'MIGRATED' And a.value = %s" % str(id)
        return self._entityManager.createQuery(sql).getSingleResult() > 0
    