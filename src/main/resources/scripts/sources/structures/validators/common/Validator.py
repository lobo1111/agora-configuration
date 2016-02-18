from base.Container import Container
from helpers.Label import LabelManager

class Validator(Container):
    _label = LabelManager()
    
    def validate(self, attribute):
        pass