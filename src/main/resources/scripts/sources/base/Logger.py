from pl.reaper.container.data import Log

class Logger:
    _svars = None
    
    def setSvars(self, svars):
        self._svars = svars
        
    def setEntityManager(self, entityManager):
        self._entityManager = entityManager

    def appendLog(self, level, message):
        log = Log()
        if self._svars != None:
            log.setThreadId(self._svars.get('_threadId'))
            log.setThreadName(self._svars.get('_threadName'))
            log.setUuid(self._svars.get('_uuid'))
            print '[JYTHON][%s][%s][%s]' % (self._svars.get('_uuid'), level, message)
        else:
            print '[JYTHON][NOT SET][%s][%s]' % (level, message)

    def info(self, message):
        self.appendLog('INFO', message)

    def warn(self, message):
        self.appendLog('WARNING', message)

    def error(self, message):
        self.appendLog('ERROR', message)