from org.eclipse.persistence.config import ResultType
from org.eclipse.persistence.config import QueryHints

class ReportManager(Container):

    def createReport(self):
        reportId = vars.get('reportId')
        report = self.getReport(reportId)
        return self.generateXML(report)

    def generateXML(self, report):
        xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
        xml += '<report>'
        for section in report.getSections():
            xml += self.generateSectionXml(report, section)
        xml += '</report>'
        return xml

    def generateSectionXml(self, report, section):
        xml = '<section>'
        data = self.getData(section.getQuery(), report.getFilters())
        for row in data:
            xml += self.generateRowXml(report, row)
        for child in section.getChildren():
            xml += self.generateSectionXml(report, child)
        xml = '</section>'
        return xml

    def generateRowXml(self, report, row):
        xml = ''
        for attribute in report.getAttributes():
            xml += '<attribute>'
            xml += '<name>'
            xml += attribute.getAttributeAlias()
            xml += '</name>'
            xml += '<value>'
            xml += row.get(attribute.getAttribute())
            xml += '</value>'
            xml += '</attribute>'
        return xml

    def getData(self, query, filters):
        queryInstance = entityManager.createQuery(query);
        queryInstance.setHint(QueryHints.RESULT_TYPE, ResultType.Map);
        return queryInstance.getResultList()

    def getReport(self, id):
        return entityManager.createQuery('Select report From Report report Where report.id = ' + str(id)).getSingleResult()