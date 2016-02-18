from base.Container import Container

class LabelManager(Container):
    
    def get(self, name):
        return unicode(self.findBy('Label', 'name', "'%s'" % name).getMessage()).encode('utf-8')