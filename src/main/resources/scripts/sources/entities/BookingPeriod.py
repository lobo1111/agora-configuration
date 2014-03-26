from base.Container import Container

class BookingPeriodManager(Container):
    
    def findAllBookingPeriods(self):
        query = 'Select period From BookingPeriod period'
        return self._entityManager.createQuery(query).getResultList()
    
    def findBookingPeriodById(self, id):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.id = ' + str(id)).getSingleResult()

    def findDefaultBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()

    def findChild(self, bookingPeriod):
        try:
            sql = 'Select period From BookingPeriod period Where period.order = ' + str(bookingPeriod.getOrder() + 1)
            return self._entityManager.createQuery(sql).getSingleResult()
        except:
            return None
    
        
    