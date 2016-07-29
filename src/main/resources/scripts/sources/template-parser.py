import helpers
helpers.init(globals())

from base.TemplateParser import TemplateParser
manager = TemplateParser()
globals()['svars'].put('output', manager.parse())