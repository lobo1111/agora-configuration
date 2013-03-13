

class CronAutoPayment(Container):
    _logger = Logger([:_scriptId])
    
    def __init__(self):
        self._logger.info('Cron auto payment started...')
        self._dictManager = DictionaryManager()
        self._documents = self.getDocuments()
        self._logger.info('Found %s documents ready for processing' % (str(self._toFire.size())))
        for document in self._document:
            self._logger.info('Processing %s' % document.getId())
            self.process(document)
            self._logger.info('Document processed')
        self._logger.info('Cron auto payment finished.')
        
    def getDocuments(self):
        sql = "Select doc From IncomingDocuments doc Where doc.status in('NEW', 'UNKNOWN')"
        return entityManager.createQuery(sql).getResultList()
    
    def process(self):
        pass