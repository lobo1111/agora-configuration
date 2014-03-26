from base.Logger import Logger

class Container:
    _logger = Logger()
    
    def __init__(self):
        self._logger.info(vars)