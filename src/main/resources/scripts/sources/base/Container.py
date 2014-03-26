from base.Logger import Logger

class Container:
    _logger = Logger()
    
    def __init__(self):
        self._logger.info('Initiated without self._svars reference')
    
    def __init__(self, svars):
        self._svars = svars
        self._logger.info(self._svars)