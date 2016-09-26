from base.Container import Container

class LabelManager(Container):
    
    def get(self, name):
        try:
            value = self.findBy('Label', 'name', "'%s'" % name).getMessage()
            self._logger.info("Label %s resolved to %s" % (name, value))
            return value
        except:
            return name