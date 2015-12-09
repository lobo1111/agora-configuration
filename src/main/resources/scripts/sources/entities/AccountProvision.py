from pl.reaper.container.data import AccountProvision
from entities.BookingPeriod import BookingPeriodManager
from base.Container import Container
from actions.AccountProvisionDocumentManager import AccountProvisionDocumentManager

class AccountProvisionManager(Container):

    def create(self):
        note = AccountProvision()
        account = self.findById("Account", self._svars.get('accountId'))
        note.setAccount(account)
        note.setCreatedAt(self.parseDate(self._svars.get('createdAt')))
        note.setProvisionValue(float(self._svars.get('value')))
        note.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
        note.setMonth(BookingPeriodManager().getCurrentMonth())
        self.saveEntity(note)
        account.getAccountProvisions().add(note)
        self._entityManager.persist(account)
        AccountProvisionDocumentManager().createDocument(note, note.getProvisionValue(), "Prowizja")
        return note

    def remove(self):
        note = self.findById("AccountProvision", self._svars.get('id'))
        if note.getInternalPayment() == None:
            self._entityManager.remove(note)
