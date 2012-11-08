class Output:
  _result = ''

  def getResult(self):
    return self._result

  def setResult(self, result):
    self._result = result

  def appendResult(self, result):
    self._result += result
output = Output()