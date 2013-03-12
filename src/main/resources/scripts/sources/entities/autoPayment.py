from pl.reaper.container.data import AutoPayment
from pl.reaper.container.data import AutoPaymentOrder

class PaymentSchedulerManager(Container):
    
    def create(self):
        autoPayment = AutoPayment()
        self.setData(autoPayment)
        entityManager.persist(autoPayment)
        
    def update(self):
        autoPayment = self.findAutoPaymentById(vars.get('id'))
        self.setData(autoPayment)
        entityManager.persist(autoPayment)
        
    def setData(self, ps):
        ps.setName(vars.get('autoPaymentName'))
        if vars.get('autoPaymentActive') == 'true':
            ps.setActive(True)
        else:
            ps.setActive(False)
        self.setZpk(ps, vars.get('autoPaymentZpkId'))
        self.setAccount(ps, vars.get('autoPaymentAccountId'))
        self.setOrders(ps, vars.get('autoPaymentOrderCount'))
        
    def setZpk(self, ps, id):
        ps.setZpk(self.findZpk(id))
        
    def setAccount(self, ps, id):
        ps.setAccount(self.findAccount(id))
        
    def setOrders(self, ps, counter):
        ps.getAutoPaymentOrders().clear()
        for i in range(int(counter)):
            zpkId = int(vars.get('autoPayemntOrderZpkId' + str(i)))
            order = int(vars.get('autoPayemntOrder' + str(i)))
            zpk = self.findZpk(zpkId)
            orderE = AutoPaymentOrder()
            orderE.setOrder(order)
            orderE.setZpk(zpk)
            ps.getAutoPaymentOrders().add(orderE)
            
        
    def findZpk(self, zpkId):
        return ZpkManager().findZpkById(zpkId)
    
    def findAccount(self, accountId):
        return AccountManager().findAccountById(accountId)
    
    def findAutoPaymentById(self, psId):
        sql = "Select ps From AutoPayment ps Where ps.id = '%s'" % psId
        return entityManager.createQuery(sql).getSingleResult()
    
    