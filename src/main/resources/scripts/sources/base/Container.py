from base.Logger import Logger

class Container:
    _logger = Logger()
    
    def setSvars(self, svars):
        self._svars = svars
        self._logger.setSvars(svars)
        self._logger.info(self._svars)
