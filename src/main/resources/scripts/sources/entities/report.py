from org.eclipse.persistence.config import ResultType
from org.eclipse.persistence.config import QueryHints

class ReportManager(Container):

    def createReport(self):
        reportName = vars.get('report')
        community = vars.get('community')
        report = self.getReport(reportName)
        return self.generateXML(report, community)

    def generateXML(self, report, community):
        xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
        xml += '<report>'
        for section in report.getSections():
            xml += self.generateSectionXml(report, section, community)
        xml += '</report>'
        return xml

    def generateSectionXml(self, report, section, community):
        xml = '<section>'
        data = self.getData(section.getQuery(), report.getFilters(), community)
        for row in data:
            xml += self.generateRowXml(report, row)
        for child in section.getChildren():
            xml += self.generateSectionXml(report, child, community)
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

    def getData(query, filters, community):
        queryInstance = entityManager.createQuery(query);
        queryInstance.setHint(QueryHints.RESULT_TYPE, ResultType.Map);
        queryInstance.setParameter('communityId', community)
        return queryInstance.getResultList()