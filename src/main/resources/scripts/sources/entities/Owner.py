from pl.reaper.container.data import Owner
from base.Container import Container
from entities.Company import CompanyManager
from entities.Person import PersonManager
from entities.Address import AddressManager

class OwnerManager(Container):

    def create(self):
        owner = new Owner()
        self.setAdditionalAddress(owner)
        self.bindPossession(owner)
        self.bindSubject(owner)
        self.saveEntity(owner)

    def setAdditionalAddress(self, owner):
        if self._svars.get('additionalAddress') == 'true':
            address = AddressManager.getAddress(None)
            owner.setAddress(address)

    def bindPossession(self, owner):
        possession = self.findById("Possession", self._svars.get('possessionId'))
        onwer.setPossession(possession)
        possession.getOwners().add(owner)
        self.saveEntity(possession)

    def bindSubject(self, owner):
        if self._svars.get('personSubject') == 'true':
            self.bindPersonSubject(owner)
        else:
            self.bindCompanySubject(owner)

    def bindPersonSubject(self, owner):
        if self._svars.get('newSubject'):
            person = PersonManager().create()
        else:
            person = self.findById('Person', self._svars.get('personId'))
        owner.setPerson(person)    

    def bindCompanySubject(self, owner):
        if self._svars.get('newSubject'):
            person = CompanyManager().create()
        else:
            person = self.findById('Company', self._svars.get('companyId'))
        owner.setCompany(company)    