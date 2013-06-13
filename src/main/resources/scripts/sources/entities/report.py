from org.eclipse.persistence.config import ResultType
from org.eclipse.persistence.config import QueryHints

class ReportManager(Container):
    _logger = Logger([:_scriptId])

    def createReport(self):
        reportId = vars.get('reportId')
        report = self.getReport(reportId)
        generatedXML = self.generateXML(report)
        output.setResult(generatedXML)
        return generatedXML

    def generateXML(self, report):
        self._logger.info('Generating report %s...' % report.getName())
        xml = ''
        xml += '<html>'
        for section in report.getSections():
            xml += self.generateSectionXml(report, section)
        xml += '</html>'
        self._logger.info('Report generated')
        return xml

    def generateSectionXml(self, report, section):
        self._logger.info('Generating section...')
        xml = '<table>'
        xml += '<tr>'
        for attribute in sorted(report.getAttributes(), key=lambda attribute: attribute.attributeOrder):
            xml += '<td>' + attribute.getAttributeAlias() + '</td>'
        xml += '</tr>'
        data = self.getData(section.getQuery())
        for row in data:
            self._logger.info('Generating section row...')
            xml += self.generateRowXml(row)
            self._logger.info('Section row generated...')
        for child in section.getChildren():
            self._logger.info('Generating section children...')
            xml += self.generateSectionXml(report, child)
            self._logger.info('Section children generated...')
        xml += '</table>'
        self._logger.info('Section generated')
        return xml

    def generateRowXml(self, row):
        xml = '<tr>'
        for attribute in row:
            xml += '<td>'
            xml += str(attribute)
            xml += '</td>'
        xml += '</tr>'
        return xml

    def getData(self, query):
        query = query.replace('{:where}', vars.get('where'))
        queryInstance = entityManager.createQuery(query);
        return queryInstance.getResultList()

    def getReport(self, id):
        return entityManager.createQuery('Select report From Report report Where report.id = ' + str(id)).getSingleResult()