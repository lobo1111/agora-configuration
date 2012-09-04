from pl.reaper.container.data import Log

class Logger:
  _scriptId = None

  def __init__(self, scriptId):
    self._scriptId = scriptId

  def appendLog(self, level, message):
    log = Log()
    log.setScriptId(self._scriptId)
    log.setThreadId(vars.get('_threadId'))
    log.setThreadName(vars.get('_threadName'))
    log.setLevel(level)
    log.setMessage(message)
    log.setUuid(vars.get('_uuid'))
    entityManager.persist(log)
    entityManager.flush()

  def info(self, message):
    self.appendLog('INFO', message)

  def warn(self, message):
    self.appendLog('WARNING', message)

  def error(self, message):
    self.appendLog('ERROR', message)