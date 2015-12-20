from base.Container import Container
from java.math import BigDecimal
from documents.Invoice import InvoiceManager
from documents.Document import DocumentManager
from pl.reaper.container.data import Document
from pl.reaper.container.data import DocumentPosition
from entities.BookingPeriod import BookingPeriodManager

class InvoiceMigrator(Container):
    
    def migrateAll(self):
        for invoice in self.collect():
            if not self.alreadyMigrated(invoice.getId()):
                self._logger.info('Migrating invoice %d...' % invoice.getId())
                document = Document()
                document.setType('INVOICE')
                document.setCommunity(invoice.getCommunity())
                document.setContractor(invoice.getContractor())
                document.setCreatedAt(invoice.getCreateDate())
                document.putAttribute('NUMBER', invoice.getNumber())
                document.putAttribute('CREATE_DATE', str(SimpleDateFormat('dd-MM-yyyy').format(invoice.getCreateDate())))
                document.putAttribute('PAYMENT_DATE', str(SimpleDateFormat('dd-MM-yyyy').format(invoice.getPaymentDate())))
                if invoice.isAccepted():
                    document.putAttribute('ACCEPTED', 'true')
                else:
                    document.putAttribute('ACCEPTED', 'false')
                document.putAttribute('MIGRATED', str(invoice.getId()))
                self.addPositions(document, invoice)
                self.addPayments(document, invoice)
                InvoiceManager().checkIfPayed(document)
                self.saveEntity(document)
            else:
                self._logger.info('Invoice %d already migrated, skipping...' % invoice.getId())
            
    def addPositions(self, document, invoice):
        for position in invoice.getPositions():
            documentPosition = DocumentPosition()
            documentPosition.setType('INVOICE_COST')
            documentPosition.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
            documentPosition.setMonth('0')
            documentPosition.setValue(BigDecimal(position.getUnitValueNet()))
            documentPosition.setBooked(False)
            documentPosition.setCreatedAt(invoice.getCreateDate())
            documentPosition.setDescription(position.getName())
            documentPosition.putAttribute('NUMBER', str(position.getPosition()))
            documentPosition.putAttribute('TAX_ID', str(position.getTax().getId()))
            documentPosition.putAttribute('VOLUME', str(position.getVolume()))
            documentPosition.putAttribute('VALUE_NET', str(position.getValueNet()))
            documentPosition.putAttribute('VALUE_GROSS', str(position.getValueGross()))
            documentPosition.setCreditZpk(DocumentManager().findZpk(document.getContractor().getZpks(), 'CONTRACTOR'))
            documentPosition.setDebitZpk(DocumentManager().findZpk(document.getContractor().getZpks(), 'CONTRACTOR_COST'))
            DocumentManager().bound(document, documentPosition)
            
    def addPayments(self, document, invoice):
        for payment in invoice.getPayments():
            documentPosition = DocumentPosition()
            documentPosition.setType('INVOICE_PAYMENT')
            documentPosition.setCreatedAt(payment.getCreateDate())
            documentPosition.setValue(BigDecimal(payment.getValuePayment()))
            documentPosition.setBooked(False)
            if(payment.getInternalPayment() != None):
                documentPosition.setBookingPeriod(payment.getInternalPayment().getBookingPeriod())
                documentPosition.setMonth(payment.getInternalPayment().getMonth())
            else:
                documentPosition.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
                documentPosition.setMonth('0')
            documentPosition.setCreditZpk(DocumentManager().findZpk(document.getCommunity().getZpks(), 'RENT'))
            documentPosition.setDebitZpk(DocumentManager().findZpk(document.getContractor().getZpks(), 'CONTRACTOR'))
            DocumentManager().bound(document, documentPosition)
   
    def collect(self):
        sql = "Select i From Invoice i"
        return self._entityManager.createQuery(sql).getResultList()
    
    def alreadyMigrated(self, id):
        sql = "Select count(a) From Document d Join d.attributes a Where d.type = 'INVOICE' And a.name = 'MIGRATED' And a.value = %s" % str(id)
        return self._entityManager.createQuery(sql).getSingleResult() > 0
    