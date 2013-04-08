class Output:
  _result = ''

  def getResult(self):
    tmp = self._result
    self._result = ''
    return tmp

  def setResult(self, result):
    self._result = result

  def appendResult(self, result):
    self._result += result
output = Output()