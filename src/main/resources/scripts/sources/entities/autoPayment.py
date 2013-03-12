from pl.reaper.container.data import AutoPayment
from pl.reaper.container.data import AutoPaymentOrder

class AutoPaymentManager(Container):
    
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
        self.clearOrders(ps)
        for i in range(int(counter)):
            id = int(vars.get('autoPayemntOrderId' + str(i)))
            orderE = self.getOrder(ps, id)
            zpkId = int(vars.get('autoPayemntOrderZpkId' + str(i)))
            order = int(vars.get('autoPayemntOrder' + str(i)))
            zpk = self.findZpk(zpkId)
            orderE.setOrder(order)
            orderE.setZpk(zpk)
            
    def getOrder(self, ps, id):
        entity = AutoPaymentOrder()
        entity.setAutoPayment(ps)
        entityManager.persist(entity)
        return entity;

    def clearOrders(self, ps):
        for order in ps.getAutoPaymentOrders():
            ps.getAutoPaymentOrders().remove(order)
            entityManager.remove(order)

    def findInList(self, orders, id):
        for entity in orders:
            if entity.getId() == id:
                return entity
        return None
        
    def findZpk(self, zpkId):
        return ZpkManager().findZpkById(zpkId)
    
    def findAccount(self, accountId):
        return AccountManager().findAccountById(accountId)
    
    def findAutoPaymentById(self, psId):
        sql = "Select ps From AutoPayment ps Where ps.id = '%s'" % psId
        return entityManager.createQuery(sql).getSingleResult()
    
    