from base.Container import Container

class BookingPeriodManager(Container):
    
    def findAllBookingPeriods(self):
        query = 'Select period From BookingPeriod period'
        return entityManager.createQuery(query).getResultList()
    
    def findBookingPeriodById(self, id):
        return entityManager.createQuery('Select period From BookingPeriod period Where period.id = ' + str(id)).getSingleResult()

    def findDefaultBookingPeriod(self):
        return entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()

    def findChild(self, bookingPeriod):
        try:
            sql = 'Select period From BookingPeriod period Where period.order = ' + str(bookingPeriod.getOrder() + 1)
            return entityManager.createQuery(sql).getSingleResult()
        except:
            return None
    
        
    