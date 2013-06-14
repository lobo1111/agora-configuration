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
        xml = '<table style="%s">' % report.getTableStyle()
        for section in sorted(report.getSections(), key=lambda section: section.sectionOrder):
            xml += self.generateSectionXml(report, section)
        xml += '</table>'
        xml += '</html>'
        self._logger.info('Report generated')
        return xml

    def generateSectionXml(self, report, section):
        xml = ''
        if section.isShowTitle():
            xml += '<tr style="%s">' % report.getTitleStyle()
            xml += '<td colspan="%d">%s</td>' %(len(report.getAttributes(), section.getTitle()))
            xml += '</tr>'
        if section.isShowHeader():
            xml += '<tr style="%s">' % report.getHeaderStyle()
            for attribute in sorted(report.getAttributes(), key=lambda attribute: attribute.attributeOrder):
                xml += '<td style="%s">%s</td>' % (attribute.getHeaderStyle(), attribute.getAttributeAlias())
            xml += '</tr>'
        data = self.getData(section.getQuery(), section.isNativeQuery())
        for row in data:
            xml += self.generateRowXml(report, row)
        for child in section.getChildren():
            xml += self.generateSectionXml(report, child)
        return xml

    def generateRowXml(self, report, row):
        xml = '<tr style="%s">' % report.getDataStyle()
        for attribute in sorted(report.getAttributes(), key=lambda attribute: attribute.attributeOrder):
            xml += '<td>'
            if row.containsKey(attribute.getAttribute()) and row.get(attribute.getAttribute()) is not None:
                xml += str(row.get(attribute.getAttribute()))
            else:
                self._logger.warn('Attribute not available or is null - %s' % attribute.getAttribute())
                xml += ''
            xml += '</td>'
        xml += '</tr>'
        return xml

    def getData(self, query, native):
        query = query.replace('{:where}', vars.get('where'))
        if native:
            queryInstance = entityManager.createNativeQuery(query);
        else:
            queryInstance = entityManager.createQuery(query);
        queryInstance.setHint(QueryHints.RESULT_TYPE, ResultType.Map);
        return queryInstance.getResultList()

    def getReport(self, id):
        return entityManager.createQuery('Select report From Report report Where report.id = ' + str(id)).getSingleResult()
