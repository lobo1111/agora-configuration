from base.Container import Container
from java.math import BigDecimal
from java.text import SimpleDateFormat
from entities.Dictionary import DictionaryManager
from documents.Document import DocumentManager
from pl.reaper.container.data import Document
from pl.reaper.container.data import DocumentPosition
from entities.BookingPeriod import BookingPeriodManager

class ChargerMigrator(Container):
    
    def migrateAll(self):
        for charging in self.collect():
            if not self.alreadyMigrated(charging.getId()):
                self._logger.info('Migrating charging %d...' % charging.getId())
                document = Document()
                document.setType('CHARGING')
                document.setCommunity(charging.getPossession().getCommunity())
                document.setPossession(charging.getPossession())
                document.setCreatedAt(charging.getTimestamp())
                document.putAttribute('CREATE_DATE', str(SimpleDateFormat('dd-MM-yyyy').format(charging.getTimestamp())))
                document.putAttribute('MIGRATED', str(charging.getId()))
                for element in charging.getChargingElements():
                    documentPosition = DocumentPosition()
                    documentPosition.setType('CHARGING_POSITION')
                    documentPosition.setCreatedAt(charging.getTimestamp())
                    documentPosition.setValue(BigDecimal(element.getValue()))
                    documentPosition.setDescription(element.getName())
                    documentPosition.putAttribute("ELEMENT_GROUP_ID", str(element.getGroup().getId()))
                    documentPosition.putAttribute("ELEMENT_GROUP_NAME", str(element.getGroup().getValue()))
                    if charging.getInternalPayment() != None:
                        documentPosition.setBookingPeriod(charging.getInternalPayment().getBookingPeriod())
                        documentPosition.setMonth(charging.getMonth())
                        documentPosition.setBooked(True)
                    else:
                        documentPosition.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
                        documentPosition.setMonth('0')
                        documentPosition.setBooked(False)
                    if self.isRepairFundElement(element):
                        documentPosition.setCreditZpk(self.findZpk(charging.getPossession().getCommunity().getZpks(), 'CHARGING_RENT'))
                        documentPosition.setDebitZpk(self.findZpk(charging.getPossession().getZpks(), 'POSSESSION'))
                    else:
                        documentPosition.setCreditZpk(self.findZpk(charging.getPossession().getCommunity().getZpks(), 'CHARGING_REPAIR_FUND'))
                        documentPosition.setDebitZpk(self.findZpk(charging.getPossession().getZpks(), 'POSSESSION_REPAIR_FUND'))
                    DocumentManager().bound(document, documentPosition)
                self.saveEntity(document)
            else:
                self._logger.info('Note %d already migrated, skipping...' % note.getId())
            
    def collect(self):
        sql = "Select i From Charging i"
        return self._entityManager.createQuery(sql).getResultList()
    
    def alreadyMigrated(self, id):
        sql = "Select count(a) From Document d Join d.attributes a Where d.type = 'CHARGING' And a.name = 'MIGRATED' And a.value = %s" % str(id)
        return self._entityManager.createQuery(sql).getSingleResult() > 0
    
    def isRepairFundElement(self, element):
        return DictionaryManager().findDictionaryInstance("PROPERTIES", "elements.repairFundGroup").getValue() == element.getGroup().getId()
    