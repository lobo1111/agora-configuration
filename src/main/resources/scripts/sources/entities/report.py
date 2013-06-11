from org.eclipse.persistence.config import ResultType
from org.eclipse.persistence.config import QueryHints

class ReportManager(Container):
    _logger = Logger([:_scriptId])

    def createReport(self):
        reportId = vars.get('reportId')
        report = self.getReport(reportId)
        return self.generateXML(report)

    def generateXML(self, report):
        self._logger.info('Generating report %s...' % report.getName())
        xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
        xml += '<report>'
        for section in report.getSections():
            xml += self.generateSectionXml(report, section)
        xml += '</report>'
        self._logger.info('Report generated')
        return xml

    def generateSectionXml(self, report, section):
        self._logger.info('Generating section...')
        xml = '<section>'
        data = self.getData(section.getQuery(), report.getFilters())
        for row in data:
            self._logger.info('Generating section row...')
            xml += self.generateRowXml(report, row)
            self._logger.info('Section row generated...')
        for child in section.getChildren():
            self._logger.info('Generating section children...')
            xml += self.generateSectionXml(report, child)
            self._logger.info('Section children generated...')
        xml = '</section>'
        self._logger.info('Section generated')
        return xml

    def generateRowXml(self, report, row):
        xml = ''
        for attribute in report.getAttributes():
            self._logger.info('Adding section attribute[%s=%s]' % (attribute.getAttribute(), attribute.getAttributeAlias()))
            xml += '<attribute>'
            xml += '<name>'
            xml += attribute.getAttributeAlias()
            xml += '</name>'
            xml += '<value>'
            if row.containsKey(attribute.getAttribute()):
                xml += str(row.get(attribute.getAttribute()))
            else:
                self._logger.warn('Attribute not available - %s' % attribute.getAttribute())
                xml += 'ATTRIBUTE NOT AVAILABLE - %s' % attribute.getAttribute()
            xml += '</value>'
            xml += '</attribute>'
        return xml

    def getData(self, query, filters):
        queryInstance = entityManager.createQuery(query);
        queryInstance.setHint(QueryHints.RESULT_TYPE, ResultType.Map);
        return queryInstance.getResultList()

    def getReport(self, id):
        return entityManager.createQuery('Select report From Report report Where report.id = ' + str(id)).getSingleResult()