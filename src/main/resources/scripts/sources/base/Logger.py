from pl.reaper.container.data import Log

class Logger:

  def appendLog(self, level, message):
    global svars
    log = Log()
    log.setThreadId(svars.get('_threadId'))
    log.setThreadName(svars.get('_threadName'))
    log.setLevel(level)
    log.setMessage(unicode(message, errors = 'replace')[0:1023])
    log.setUuid(svars.get('_uuid'))
    print '[JYTHON][%s][%s][%s]' % (svars.get('_uuid'), level, message)
    if level in ['WARNING', 'ERROR']:
        entityManager.persist(log)

  def info(self, message):
    self.appendLog('INFO', message)

  def warn(self, message):
    self.appendLog('WARNING', message)

  def error(self, message):
    self.appendLog('ERROR', message)