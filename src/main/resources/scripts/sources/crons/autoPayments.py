

class CronAutoPayment(Container):
    _logger = Logger([:_scriptId])
    
    def __init__(self):
        self._logger.info('Cron auto payment started...')
        self._dictManager = DictionaryManager()
        self._documents = self.getDocuments()
        self._logger.info('Found %s documents ready for processing' % (str(self._documents.size())))
        for document in self._documents:
            self._logger.info('Processing document - id:%s' % document.getId())
#            self.process(document)
            self._logger.info('Document processed')
        self._logger.info('Cron auto payment finished.')
        
    def getDocuments(self):
        sql = "Select doc From IncomingPaymentDocument doc Where doc.status in('NEW', 'UNKNOWN')"
        return entityManager.createQuery(sql).getResultList()
    
    def process(self, document):
        autoPayment = self.matchAutoPayment(document)
        if autoPayment is None:
            self._logger.info("Can't match this document to any account.")
            self.setAsUnknown(document)
        else:  
            self._logger.info("Document matched, creating payments....")
            self.createPayments(document)
            self.setAsProcessed(document)
        entityManager.persist(document)
        
    def matchAutoPayment(self, document):
        try:
            sql = 'Select auto From AutoPayment auto Join auto.account account Where account.number = %s' % document.getAccountNumber()
            return entityManager.createQuery(sql).getSingleResult()
        except:
            return None;
        
    def setAsUnknown(self, document):
        document.setStatus('UNKNOWN')
    
    def setAsProcessed(self, document):
        document.setStatus('PROCESSED')
    
    def createPayments(self, document):
        pass
    
        