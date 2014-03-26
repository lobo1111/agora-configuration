from base.Logger import Logger

global svars

class Container:
    _logger = Logger()
    
    def __init__(self):
        self._logger.info(svars)