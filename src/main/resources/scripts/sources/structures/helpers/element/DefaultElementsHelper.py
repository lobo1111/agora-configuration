from base.Container import Container
from pl.reaper.container.data import ElementCommunity

class DefaultElementsHelper(Container):
    
    def createDefaultElementsForCommunity(self, community):
        for element in self.collectDefaultElements():
            communityElement = ElementCommunity()
            communityElement.setElement(element)
            communityElement.setCommunity(community)
            community.getElements().add(communityElement)
            
    def collectDefaultElements(self):
        sql = 'Select e from Element e Where e.defaultElement = true'
        return self._entityManager.createQuery(sql).getResultList()