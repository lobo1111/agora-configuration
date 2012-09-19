class TemplateParser(Container):
    
    def __init__(self):
        self._templateName = vars.get('templateName')
    
    def parse(self):
        result = templateBean.getTemplate(self._templateName)
        output.setResult(result)
        