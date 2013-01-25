class BookingPeriodManager(Container):
    _logger = Logger([:_scriptId])
    
    def findAllBookingPeriods(self):
        query = 'Select period From BookingPeriod period'
        return entityManager.createQuery(query).getResultList()
    
        
    