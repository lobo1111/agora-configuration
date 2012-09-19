class TemplateParser(Container):
    
    def parseTemplate(self, templateName):
        output.setResult(templateBean.getTemplate(templateName))