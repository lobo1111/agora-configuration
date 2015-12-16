import helpers
helpers.init(globals())

from base.TemplateParser import TemplateParser
manager = TemplateParser()
helpers.svars.put('output', manager.parse())