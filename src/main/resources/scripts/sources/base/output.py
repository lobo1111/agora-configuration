class Output:
  _result = ''
  
  def __init__(self):
      global outputAsString
      self._result = outputAsString

  def getResult(self):
    tmp = self._result
    self._result = ''
    return tmp

  def setResult(self, result):
    self._result = result

  def appendResult(self, result):
    self._result += result
output = Output()