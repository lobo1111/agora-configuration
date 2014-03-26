from base.TemplateParser import TemplateParser

global svars, entityManager, properties
manager = TemplateParser()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
self._svars.put('output', manager.parse())