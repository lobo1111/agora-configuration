class ElementMapper(Mapper):
    
    def initStructure(self):
        if int(self.get('id')) > 0:
            self._logger.info("Element persist - it's an update. Found id: %s, of type" % (self.get('id'), self.get('type')))
            self._entity = self.loadEntity(self.get('type'), int(self.get('id')))
            self._isNew = False
        else:
            self._logger.info("Account persist - it's a new account")
            self._entity = self.initEntity(int(self.get('type')))
            self._isNew = True
            
    def setData(self):
        if self.hasAttribute("algorithm"):
            self.map("algorithm", [DictionaryValidator(dictionary="ELEMENT_ALGORITHMS", messageParameter="Algorytm")])
        if self.hasAttribute("group"):
            self.map("group", [DictionaryValidator(dictionary="ELEMENTS", messageParameter="Grupa")])
        if self.hasAttribute("name"):
            self.map("name", [LengthValidator(minLength=1, maxLength=255, messageParameter="Nazwa składnika")])
        if self.hasAttribute("globalValue"):
            self.map("globalValue", [DecimalValidator(messageParameter="Wartość")])
        if self.hasAttribute("defaultElement"):
            self.map("defaultElement")
        if self.hasAttribute("overrideParentValue"):
            self.map("overrideParentValue")
            
    def loadEntity(self, type, id):
        if type == 'GLOBAL':
            return self.findById("Element", id)
        elif type == 'COMMUNITY':
            return self.findById("ElementCommunity", id)
        elif type == 'POSSESSION':
            return self.findById("ElementPossession", id)
        else:
            return None
        
    def initEntity(self, type):
        if type == 'GLOBAL':
            return Element()
        elif type == 'COMMUNITY':
            return ElementCommunity()
        elif type == 'POSSESSION':
            return ElementPossession()
        else:
            return None