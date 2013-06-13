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
        xml = '<table style="%s">' % report.getTableStyle()
        xml += '<tr>'
        for attribute in sorted(report.getAttributes(), key=lambda attribute: attribute.attributeOrder):
            xml += '<td style="%s">%s</td>' % (report.getHeaderStyle(), attribute.getAttributeAlias())
        xml += '</tr>'
        data = self.getData(section.getQuery())
        for row in data:
            xml += self.generateRowXml(report, row)
        for child in section.getChildren():
            xml += self.generateSectionXml(report, child)
        xml += '</table>'
        return xml

    def generateRowXml(self, report, row):
        xml = '<tr>'
        for attribute in sorted(report.getAttributes(), key=lambda attribute: attribute.attributeOrder):
            xml += '<td style="%s">' % report.getDataStyle()
            if row.containsKey(attribute.getAttribute()):
                xml += str(row.get(attribute.getAttribute()))
            else:
                self._logger.warn('Attribute not available - %s' % attribute.getAttribute())
                xml += ''
            xml += '</td>'
        xml += '</tr>'
        return xml

    def getData(self, query):
        query = query.replace('{:where}', vars.get('where'))
        queryInstance = entityManager.createQuery(query);
        queryInstance.setHint(QueryHints.RESULT_TYPE, ResultType.Map);
        return queryInstance.getResultList()

    def getReport(self, id):
        return entityManager.createQuery('Select report From Report report Where report.id = ' + str(id)).getSingleResult()