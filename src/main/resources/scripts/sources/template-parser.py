class TemplateParser(Container):
    
    def __init__(self, templateName):
        self_templateName = templateName
    
    def parseTemplate(self):
        output.setResult(templateBean.getTemplate(self._templateName))
        