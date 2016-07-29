from base.Container import Container

class ValueHelper(Container):
    
    def getValue(self, element):
        if self.isPossessionElement(element):
            if element.isOverrideParentValue():
                return element.getGlobalValue()
            else:
                if element.getCommunityElement() != None:
                    element = element.getCommunityElement()
                else:
                    element = element.getElement()
        elif self.isCommunityElement(element):
            if element.isOverrideParentValue():
                return element.getGlobalValue()
            else:
                element = element.getElement()
        else:
            return element.getGlobalValue()
        
    def isPossessionElement(self, element):
        return element.getClass().getName() == "pl.reaper.container.data.ElementPossession"
    
    def isCommunityElement(self, element):
        return element.getClass().getName() == "pl.reaper.container.data.ElementCommunity"
    
                
            