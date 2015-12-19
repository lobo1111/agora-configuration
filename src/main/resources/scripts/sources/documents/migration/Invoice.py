from pl.reaper.container.data import Document
from pl.reaper.container.data import DocumentPosition

class InvoiceMigrator(Container):
    
    def migrateAll(self):
        for invoice in collect():
            document = Document()
            document.setType('INVOICE')
            document.setCommunity(invoice.getCommunity())
            document.setContractor(invoice.getContractor())
            document.setCreatedAt(invoice.getCreateDate())
            document.putAttribute('NUMBER', invoice.getNumber())
            document.putAttribute('CREATE_DATE', str(invoice.getCreateDate()))
            document.putAttribute('ACCEPTED', str(invoice.isAccepted()))
            document.putAttribute('PAYED', str(invoice.isPayed()))
            document.putAttribute('MIGRATED', str(invoice.getId()))
            self.addPositions(document, invoice)
            self.addPayments(document, invoice)
            self.saveEntity(document)
            
    def addPositions(self, document, invoice):
        for position in invoice.getPositions():
            documentPosition = DocumentPosition()
            documentPosition.setType('INVOICE_COST')
            documentPosition.setBookingPeriod(invoice.getBookingPeriod())
            documentPosition.setMonth(0)
            documentPosition.setValue(position.getUnitValueNet())
            documentPosition.setBooked(False)
            documentPosition.setCreatedAt(invoice.getCreateDate())
            documentPosition.setDescription(position.getName())
            documentPosition.putAttribute('NUMBER', str(position.getPosition()))
            documentPosition.putAttribute('TAX_ID', str(position.getTax().getId()))
            documentPosition.putAttribute('VOLUME', str(position.getVolume()))
            documentPosition.putAttribute('VALUE_NET', str(position.getValueNet()))
            documentPosition.putAttribute('VALUE_GROSS', str(position.getValueGross()))
            documentPosition.setCreditZpk(document.findZpk(document.getContractor().getZpks(), 'CONTRACTOR'))
            documentPosition.setDebitZpk(document.findZpk(document.getContractor().getZpks(), 'CONTRACTOR_COST'))
            documentPosition.setDocument(document)
            
    def addPayments(self, document, invoice):
        for payment in invoice.getPayments():
            documentPosition = DocumentPosition()
            documentPosition.setType('INVOICE_PAYMENT')
            documentPosition.setCreatedAt(payment.getCreateDate())
            documentPosition.setValue(payment.getValuePayment())
            documentPosition.setBooked(False)
            documentPosition.setCreditZpk(document.findZpk(document.getCommunity().getZpks(), 'RENT'))
            documentPosition.setDebitZpk(document.findZpk(document.getContractor().getZpks(), 'CONTRACTOR'))
            documentPosition.setDocument(document)
    
    def collect(self):
        sql = "Select i From Invoice i Where i.id Not In (Select attr.value From Document d Join d.attributes attr Where d.type = 'INVOICE' And attr.name = 'MIGRATED')"
        return self._entityManager.createQuery(sql).getResultList()
    