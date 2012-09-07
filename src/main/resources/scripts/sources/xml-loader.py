from xml.etree.ElementTree import fromstring
from xml.etree.ElementTree import tostring
from pl.reaper.container.data import IncomingPaymentDocument
from pl.reaper.container.data import IncomingPaymentDocumentPosition
from java.text import SimpleDateFormat
from java.math import BigDecimal

class XMLLoader(Container):

  _logger = Logger([:_scriptId])

  def process(self, content):
    self._logger.info('Processing XML...')
    xml = self.initXML(content)
    document = IncomingPaymentDocument()
    self.setHeader(xml, document)
    self.setPositions(xml, document)
    self._logger.info('XML processed')
    return True

  def initXML(self, content):
    xml = fromstring(content)
    self._logger.info('Got ' + tostring(xml))
    return xml

  def saveDocument(self, document):
    self._logger.info('Saving entity...')
    entityManager.persist(document)

  def setHeader(self, xml, document):
    self._logger.info('Setting header...')
    document.setSender(self.getText(xml, properties.getProperty('bpPathSender')))
    document.setDateFrom(self.parseDate(self.getText(xml, properties.getProperty('bpPathDateFrom'))))
    document.setDateTo(self.parseDate(self.getText(xml, properties.getProperty('bpPathDateTo'))))
    document.setAccountNumber(self.getText(xml, properties.getProperty('bpPathAccountNumber')))
    document.setExtractNumber(self.getText(xml, properties.getProperty('bpPathExtractNumber')))
    document.setIncome(BigDecimal(self.getText(xml, properties.getProperty('bpPathIncome'))))
    document.setSpending(BigDecimal(self.getText(xml, properties.getProperty('bpPathSpending'))))
    document.setPositionCounter(int(self.getText(xml, properties.getProperty('bpPathPositionCounter'))))
    document.setStatus(self.getStatus())
    self.saveDocument(document)

  def setPositions(self, xml, document):
    self._logger.info('Setting positions...')
    for xmlPosition in self.getChildren(xml, properties.getProperty('bpPathPositions')):
      position = IncomingPaymentDocumentPosition()
      position.setPositionNo(int(self.getText(xmlPosition, properties.getProperty('bpPathPositionPositionNo'))))
      position.setIncome(BigDecimal(self.getText(xmlPosition, properties.getProperty('bpPathPositionIncome'))))
      position.setClientNumber(self.getText(xmlPosition, properties.getProperty('bpPathPositionClientNumber')))
      position.setRequestDate(self.parseDate(self.getText(xmlPosition, properties.getProperty('bpPathPositionRequestDate'))))
      position.setBookingDate(self.parseDate(self.getText(xmlPosition, properties.getProperty('bpPathPositionBookingDate'))))
      position.setTitle(self.getText(xmlPosition, properties.getProperty('bpPathPositionTitle')))
      position.setClientName(self.getText(xmlPosition, properties.getProperty('bpPathPositionClientName')))
      position.setClientAddress(self.getText(xmlPosition, properties.getProperty('bpPathPositionClientAddress')))
      position.setClientAccountNumber(self.getText(xmlPosition, properties.getProperty('bpPathPositionClientAccountNumber')))
      position.setDocument(document)
      self.saveDocument(position)
      
  def getStatus(self):
    status = documentStatusLoader.getStatus(properties.getProperty('bpNewDocumentStatus'))
    self._logger.info('status=[id:%d][key:%s]' % (status.getId(), status.getKey()))
    return status

  def parseDate(self, dateAsString):
    return SimpleDateFormat(properties.getProperty('dateFormat')).parse(dateAsString)

  def getNode(self, xml, path):
    return xml.find(path)

  def getChildren(self, xml, path):
    return xml.findall(path)

  def getText(self, xml, path):
    node = self.getNode(xml, path)
    if node != None and node.text != None:
      text = node.text
      self._logger.info('path[' + path + ']=' + text.decode('cp1250'))
      return text.decode('cp1250')
    else:
      self._logger.info('path[' + path + ']=<null>')
      return ""