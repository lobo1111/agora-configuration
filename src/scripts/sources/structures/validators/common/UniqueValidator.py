from base.Container import Container
from structures.validators.common.Validator import Validator
from structures.validators.common.ValidationError import ValidationError

class UniqueValidator(Validator):
    _message = "validators.common.notUniqueField"
    
    def __init__(self, entity, attribute, id = -1, messageParameter = ''):
        self._entity = entity
        self._attribute = attribute
        self._id = int(id)
        self._messageParameter = messageParameter
    
    def validate(self, value):
        entities = Container().findAllBy(self._entity, self._attribute, "'" + value + "'")
        for entity in entities:
            if entity.getId() != self._id:
                raise ValidationError(self._label.get(self._message) % self._messageParameter)