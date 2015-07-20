from pl.reaper.container.data import AccountProvision
from entities.BookingPeriod import BookingPeriodManager
from base.Container import Container

class AccountProvisionManager(Container):

    def create(self):
        note = AccountProvision()
        note.setAccount(self.findById("Account", self._svars.get('accountId')))
        note.setCreatedAt(self.parseDate(self._svars.get('createdAt')))
        note.setProvisionValue(float(self._svars.get('value')))
        note.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
        note.setMonth(BookingPeriodManager().getCurrentMonth())
        self.saveEntity(note)

    def remove(self):
        note = self.findById("AccountProvision", self._svars.get('id'))
        if note.getInternalPayment() == None:
            self._entityManager.remove(note)
