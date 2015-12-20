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
                note = Document()
                note.setType('BANK_NOTE')
                note.setCommunity(note.getCommunity())
                note.setPossession(note.getPossession())
                note.setCreatedAt(note.getCreatedAt())
                note.setDescription(note.getDescription())
                note.putAttribute('MIGRATED', str(note.getId()))
                notePosition = DocumentPosition()
                notePosition.setType('BANK_NOTE')
                notePosition.setCreatedAt(note.getCreatedAt())
                if note.getInternalPayment() != None:
                    notePosition.setBookingPeriod(note.getInternalPayment().getBookingPeriod())
                    notePosition.setMonth(note.getInternalPayment().getMonth())
                    notePosition.setBooked(True)
                else:
                    notePosition.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
                    notePosition.setMonth('0')
                    notePosition.setBooked(False)
                notePosition.setDescription(note.getElement().getName())
                notePosition.putAttribute("ELEMENT_GROUP", note.getElement().getGroup().getValue())
                notePosition.setCreditZpk(DocumentManager().findZpk(note.getCommunity().getZpks(), 'CHARGING_RENT'))
                notePosition.setDebitZpk(DocumentManager().findZpk(note.getPossession().getZpks(), 'POSSESSION'))
                self.bound(note, notePosition)
                self.saveEntity(note)
            else:
                self._logger.info('Note %d already migrated, skipping...' % note.getId())
            
    def collect(self):
        sql = "Select i From BankNote i"
        return self._entityManager.createQuery(sql).getResultList()
    
    def alreadyMigrated(self, id):
        sql = "Select count(a) From Document d Join d.attributes a Where d.type = 'BANK_NOTE' And a.name = 'MIGRATED' And a.value = %s" % str(id)
        return self._entityManager.createQuery(sql).getSingleResult() > 0
    