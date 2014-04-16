class Initializator:
    
    def moduleInitialize(self, name):
        module = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            module = getattr(module, comp)
        return module
    
    def objectInitialize(self, name):
        module = self.moduleInitialize(name)
        name = name[name.rfind(".") + 1:]
        if name != '__init__' and hasattr(module, name):
            try:
                return getattr(module, name)()
            except TypeError:
                print "Object %s not initialized due to lack of standard constructor" % name
        else:
            print "Object %s not initialized due to lack of class definition"