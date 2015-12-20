from java.text import SimpleDateFormat
from base.Container import Container
from java.math import BigDecimal
from documents.Invoice import InvoiceManager
from documents.Document import DocumentManager
from pl.reaper.container.data import Document
from pl.reaper.container.data import DocumentPosition
from entities.BookingPeriod import BookingPeriodManager

class BankNoteMigrator(Container):
    
    def migrateAll(self):
        for note in self.collect():
            if not self.alreadyMigrated(note.getId()):
                self._logger.info('Migrating note %d...' % note.getId())
                document = Document()
                document.setType('BANK_NOTE')
                document.setCommunity(note.getPossession().getCommunity())
                document.setPossession(note.getPossession())
                document.setCreatedAt(note.getCreatedAt())
                document.setDescription(note.getDescription())
                document.putAttribute('MIGRATED', str(note.getId()))
                documentPosition = DocumentPosition()
                documentPosition.setType('BANK_NOTE')
                documentPosition.setCreatedAt(note.getCreatedAt())
                if note.getInternalPayment() != None:
                    documentPosition.setBookingPeriod(note.getInternalPayment().getBookingPeriod())
                    documentPosition.setMonth(note.getMonth())
                    documentPosition.setBooked(True)
                else:
                    documentPosition.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
                    documentPosition.setMonth('0')
                    documentPosition.setBooked(False)
                documentPosition.setDescription(note.getElement().getName())
                documentPosition.putAttribute("ELEMENT_GROUP", note.getElement().getGroup().getValue())
                documentPosition.setCreditZpk(DocumentManager().findZpk(note.getCommunity().getZpks(), 'CHARGING_RENT'))
                documentPosition.setDebitZpk(DocumentManager().findZpk(note.getPossession().getZpks(), 'POSSESSION'))
                self.bound(document, documentPosition)
                self.saveEntity(document)
            else:
                self._logger.info('Note %d already migrated, skipping...' % note.getId())
            
    def collect(self):
        sql = "Select i From BankNote i"
        return self._entityManager.createQuery(sql).getResultList()
    
    def alreadyMigrated(self, id):
        sql = "Select count(a) From Document d Join d.attributes a Where d.type = 'BANK_NOTE' And a.name = 'MIGRATED' And a.value = %s" % str(id)
        return self._entityManager.createQuery(sql).getSingleResult() > 0
    