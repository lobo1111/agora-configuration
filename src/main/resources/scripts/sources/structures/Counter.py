class Counter(Container):
    
    def persist(self):
        try:
            mapper = CounterMapper()
            mapper.initStructure()
            if mapper.isNew():
                mapper.setData()
            else:
                mapper.replace()
            self.saveEntity(mapper.getEntity())
        except ValidationError, error:
            self.setError(error)