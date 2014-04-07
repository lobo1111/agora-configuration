import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from base.TemplateParser import TemplateParser
manager = TemplateParser()
svars.put('output', manager.parse())