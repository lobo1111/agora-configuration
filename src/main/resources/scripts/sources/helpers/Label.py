from base.Container import Container

class LabelManager(Container):
    
    def get(self, name):
        return self.findBy('Label', 'name', "'name'").getMessage()