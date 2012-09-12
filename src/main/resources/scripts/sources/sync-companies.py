from pl.reaper.container.data import Address
from pl.reaper.container.data import Company

class SyncCompanies(Sync):
    _logger = Logger([:_scriptId])
    _processed = 0
    _inserted = 0
    _updated = 0
    
    def sync(self):
        self._logger.info('synchronizing companies')
        companies = self.loadData('SELECT w FROM Platnicy w WHERE w.nazwa != "None"')
        for company in companies:
            self._processed += 1
            self._logger.info('processing company %s' % company.getNazwa())
            if self.companyExists(comapny):
                self._logger.info('company exists, updating')
                self.companyUpdate(comapny)
                self._updated += 1
            else:
                self._logger.info('company doesn\'t exists, inserting')
                self.companyInsert(comapny)
                self._inserted += 1
        self._logger.info('companies synchronized[processed:%d][inserted:%d][updated:%d]' % (self._processed, self._inserted, self._updated))

    def companyExists(self, company):
        return self.syncDataExists('sync_company', 'access_company_id', company.getId())
    
    def companyUpdate(self, oldCompany):
        id = self.findBaseId('sync_company', 'erp_company_id', 'access_company_id', oldCompany.getId())
        company = self.find('Company', id)
        self.setDataAndPersistCompany(oldCompany, company)
    
    def companyInsert(self, oldCompany):
        company = Company()
        self.setDataAndPersistCompany(oldCompany, company)
        self._logger.info('new company bound: %d <-> %d' % (oldCompany.getId(), company.getId()))
        entityManager.createNativeQuery('INSERT INTO sync_company(`erp_company_id`, `access_company_id`) VALUES(%d, %d)' % (company.getId(), oldCompany.getId())).executeUpdate()
        
    def setDataAndPersistcompany(self, oldCompany, company):
        self.setAddress(oldCompany, company)
        self.setCompany(oldCompany, company)
        entityManager.flush()
        
    def setAddress(self, oldCompany, company):
        address = None
        if company.getAddress() != None:
            address = company.getAddress()
        else:
            address = Address()
        address.setStreet(self.findStreet(oldCompany.getKul()))
        address.setHouseNumber(oldCompany.getNrbr())
        address.setFlatNumber(oldCompany.getNrmie())
        address.setPostalCode(oldCompany.getKod())
        address.setCity('Swidnica')
        entityManager.persist(address)
        company.setAddress(address)
    
    def setCompany(self, oldCompany, company):
        company.setName(oldCompany.getNazwa())
        company.setPhoneNumber1(oldCompany.getTel())
        company.setNip(oldCompany.getNip())
        entityManager.persist(company)
     