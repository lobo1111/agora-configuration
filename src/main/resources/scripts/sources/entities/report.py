from org.eclipse.persistence.config import ResultType
from org.eclipse.persistence.config import QueryHints

class HTML:
    def openHTML(self):
        return '<html>'

    def closeHTML(self):
        return '</html>'

    def openTable(self, style):
        return '<table style="%s">' % style

    def closeTable(self):
        return '</table>'

    def openTd(self, colspan, style):
        return '<td colspan="%s" style="%s">' % (str(colspan), style)

    def openTd(self, style):
        return '<td style="%s">' % style

    def closeTd(self):
        return '</td>'

    def openTr(self, style):
        return '<tr style="%s">' % style

    def closeTr(self):
        return '</tr>'

    def openHeader(self):
        return '<head>'

    def closeHeader(self):
        return '</head>'

    def openScript(self):
        return '<script type="text/javascript">'

    def closeScript(self):
        return '</script>'

    def openStyle(self):
        return '<style type="text/css">'

    def closeStyle(self):
        return '</style>'

    def openBody(self, onInit):
        return '<body oninit="%s">' % onInit

    def closeBody(self):
        return '</body>'

class ReportManager(Container):
    _logger = Logger([:_scriptId])
    _html = HTML()

    def createReport(self):
        reportId = vars.get('reportId')
        report = self.getReport(reportId)
        generatedXML = self.generateXML(report)
        output.setResult(generatedXML)
        return generatedXML

    def generateXML(self, report):
        xml = self._html.openHTML()
        xml += self.addHeaderData(report)
        xml += self._html.openBody(report.getOnInit())
        for section in sorted(report.getSections(), key=lambda section: section.sectionOrder):
            xml += self.generateSectionXml(section)
        xml += self._html.closeBody()
        xml += self._html.closeHTML()
        return xml

    def addHeaderData(self, report):
        xml = ''
        xml += self._html.openHeader()
        xml += self._html.openScript()
        if report.getJs() is not None:
            xml += report.getJs()
        xml += self._html.closeScript()
        xml += self._html.openStyle()
        if report.getCss() is not None:
            xml += report.getCss()
        xml += self._html.closeStyle()
        xml += self._html.closeHeader()
        return xml;

    def generateSectionXml(self, section):
        xml = ''
        xml += self._html.openTable(section.getTableStyle())
        xml += self.renderSectionTitle(section)
        xml += self.renderSectionHeader(section)
        xml += self.renderSectionData(section)
        xml += self.renderSectionChildren(section)
        xml += self._html.closeTable()
        return xml

    def generateRowXml(self, section, row):
        xml = self._html.openTr(section.getRowStyle())
        for attribute in sorted(section.getAttributes(), key=lambda attribute: attribute.attributeOrder):
            xml += self._html.openTd(attribute.getColumnStyle())
            if row.containsKey(attribute.getAttribute()) and row.get(attribute.getAttribute()) is not None:
                xml += str(row.get(attribute.getAttribute()))
            else:
                self._logger.warn('Attribute not available or is null - %s' % attribute.getAttribute())
                xml += ''
            xml += self._html.closeTd()
        xml += self._html.closeTr()
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

    def renderSectionTitle(self, section):
        xml = ''
        if section.isShowTitle():
            xml += self._html.openTr(section.getTitleStyle())
            xml += self._html.openTd(len(report.getAttributes(), ''))
            xml += section.getTitle()
            xml += self._html.closeTd()
            xml += self._html.closeTr()
        return xml

    def renderSectionHeader(self, section):
        xml = ''
        if section.isShowHeader():
            xml += self._html.openTr('')
            for attribute in sorted(section.getAttributes(), key=lambda attribute: attribute.attributeOrder):
                xml += self._html.openTd(attribute.getHeaderStyle())
                xml += attribute.getAttributeAlias()
                xml += self._html.closeTd()
            xml += self._html.closeTr()
        return xml

    def renderSectionData(self, section):
        xml = ''
        for row in self.getData(section.getQuery(), section.isNativeQuery()):
            xml += self.generateRowXml(section, row)
        return xml

    def renderSectionChildren(self, section):
        xml = ''
        for child in section.getChildren():
            xml += self.generateSectionXml(child)
        return xml
    
