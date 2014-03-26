from base.TemplateParser import TemplateParser

global svars, entityManager, properties
manager = TemplateParser()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
svars.put('output', manager.parse())