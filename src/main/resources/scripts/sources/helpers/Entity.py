from javax.naming import InitialContext

class Entity:

    def persist(self, entity):
        context = InitialContext()
        entityManager = context.lookup("java:comp/env/persistence/agora_erp")
        entityManager.persist(entity)


