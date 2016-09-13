from base.Container import Container
from helpers.Label import LabelManager

class Validator(Container):
    _label = LabelManager()
    
    def validate(self, document):
        pass
    
    def check(self, attribute, validators):
        for validator in validators:
            validator.validate(attribute)