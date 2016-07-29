from base.Container import Container

class LabelManager(Container):
    
    def get(self, name):
        #value = unicode(self.findBy('Label', 'name', "'%s'" % name).getMessage()).encode('utf8')
        value = self.findBy('Label', 'name', "'%s'" % name).getMessage()
        self._logger.info("Label %s resolved to %s" % (name, value))
        return value