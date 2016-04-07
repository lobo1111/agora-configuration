from base.Container import Container
from structures.helpers.counter.Mapper import CounterMapper
from structures.validators.common.ValidationError import ValidationError

class CounterManager(Container):
    
    def persist(self):
        try:
            mapper = CounterMapper()
            mapper.initStructure()
            if mapper.get('counterType') in ['LOCAL', 'GLOBAL']:
                mapper.setData()
            elif mapper.get('counterType') in ['REPLACE']:
                mapper.replace()
            self.saveEntity(mapper.getEntity())
        except ValidationError, error:
            self.setError(error)