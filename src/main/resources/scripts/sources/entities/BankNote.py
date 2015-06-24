from pl.reaper.container.data import BankNote
from entities.BookingPeriod import BookingPeriodManager
from base.Container import Container

class BankNoteManager(Container):

    def create(self):
        note = BankNote()
        note.setPossession(self.findById("Possession", self._svars.get('possessionId')))
        note.setElement(self.findById("Element", self._svars.get('elementId')))
        note.setCreatedAt(self.parseDate(self._svars.get('createdAt')))
        note.setNoteValue(float(self._svars.get('value')))
        note.setDescription(self._svars.get('description'))
        note.setBookingPeriod(BookingPeriodManager().findDefaultBookingPeriod())
        note.setMonth(self.getCurrentMonth())
        self.saveEntity(note)

    def remove(self):
        note = self.findById("BankNote", self._svars.get('id'))
        if note.getInternalPayment() == None:
            self._entityManager.remove(note)

    def getCurrentMonth(self):
        return self._entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
    
