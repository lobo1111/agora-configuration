import helpers
helpers.init(globals())

from base.TemplateParser import TemplateParser
manager = TemplateParser()
svars.put('output', manager.parse())