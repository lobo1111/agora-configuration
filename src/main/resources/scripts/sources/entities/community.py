from pl.reaper.container.data import Community

class CommunityManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        community = Community()
        self.setCommunityData(community)
        self.saveCommunity(community)
        
    def update(self):
        community = self.findCommunity()
        self.setCommunityData(community)
        self.saveCommunity(community)
        
    def setCommunityData(self, community):
        community.setName(vars.get('name'))
        company.setCompany(self.getCompany(community))
        
    def getCompany(self, community):
        companyManager = companyManager()
        return companyManager.getCompany(community)
        
    def saveCommunity(self, community):
        self._logger.info(community.longDescription())
        entityManager.persist(community)
        entityManager.flush()
        
    def findCommunity(self):
        id = vars.get('id')
        return entityManager.createQuery('Select community From Community community Where community.id = ' + id).getSingleResult()