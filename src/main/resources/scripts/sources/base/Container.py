from base.Logger import Logger

class Container:
    _logger = Logger()
    
    def __init__(self):
        global svars
        self._logger.info(svars)