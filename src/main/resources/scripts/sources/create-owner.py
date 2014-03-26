from entities.Owner import OwnerManager

global svars, entityManager, properties
ownerManager = OwnerManager()
ownerManager.setSvars(svars)
ownerManager.setEntityManager(entityManager)
ownerManager.setProperties(properties)
ownerManager.create()