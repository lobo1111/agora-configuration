class TemplateParser(Container):
    
    def parseTemplate(self, templateName):
        return templateBean.getTemplate(templateName)