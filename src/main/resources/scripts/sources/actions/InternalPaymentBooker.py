class InternalPaymentBooker(Container):
    
     def bookAll(self):
         manager = InternalPaymentManager()
        [manager.book(payment) for payment in self.collectPayments()]
        
    def collectPayments(self):
        sql = 'Select i From InternalPayment Where i.booked = false'
        return self._entityManager.createQuery(sql).getResultList()
        