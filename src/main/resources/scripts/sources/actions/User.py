from base.Container import Container

class User(Container):
    
    def getUserInformation(self):
        person = self.collectUser()
        output = self.parseOutput(person)
        self._svars.put('output', output)
        return userName
    
    def collectUser(self):
        login = self._context.getUserPrincipal().getName()
        self._logger.info("Collection username for login information %s" % login)
        sql = 'Select person From Person person Join person.users user Where user.login = %s' % login
        person = self._entityManager.createQuery(sql).getSingleResult()
        return person
    
    def parseOuput(self, person):
        template = self.findBy("Template", "name", "'user-information'")
        ve = VelocityEngine()
        ve.init()
        context = VelocityContext()
        context.put("person", person)
        writer = StringWriter()
        ve.evaluate(context, writer, template.getName(), unicode(template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate