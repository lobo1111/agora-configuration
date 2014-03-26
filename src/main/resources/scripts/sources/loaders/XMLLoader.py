from xml.etree.ElementTree import fromstring
from xml.etree.ElementTree import tostring
from pl.reaper.container.data import IncomingPaymentDocument
from pl.reaper.container.data import IncomingPaymentDocumentPosition
from java.text import SimpleDateFormat
from java.math import BigDecimal
from base.Container import Container
from entities.Dictionary import DictionaryManager

class XMLLoader(Container):

  def __init__(self):
    self._dictManager = DictionaryManager()

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
    self._entityManager.persist(document)

  def setHeader(self, xml, document):
    self._logger.info('Setting header...')
    document.setSender(self.getText(xml, self._properties.getProperty('bpPathSender')))
    document.setDateFrom(self.parseDate(self.getText(xml, self._properties.getProperty('bpPathDateFrom'))))
    document.setDateTo(self.parseDate(self.getText(xml, self._properties.getProperty('bpPathDateTo'))))
    document.setAccountNumber(self.getText(xml, self._properties.getProperty('bpPathAccountNumber')))
    document.setExtractNumber(self.getText(xml, self._properties.getProperty('bpPathExtractNumber')))
    document.setIncome(BigDecimal(self.getText(xml, self._properties.getProperty('bpPathIncome'))))
    document.setSpending(BigDecimal(self.getText(xml, self._properties.getProperty('bpPathSpending'))))
    document.setPositionCounter(int(self.getText(xml, self._properties.getProperty('bpPathPositionCounter'))))
    self.saveDocument(document)

  def setPositions(self, xml, document):
    self._logger.info('Setting positions...')
    for xmlPosition in self.getChildren(xml, self._properties.getProperty('bpPathPositions')):
      position = IncomingPaymentDocumentPosition()
      position.setPositionNo(int(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionPositionNo'))))
      position.setIncome(BigDecimal(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionIncome'))))
      position.setClientNumber(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionClientNumber')))
      position.setRequestDate(self.parseDate(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionRequestDate'))))
      position.setBookingDate(self.parseDate(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionBookingDate'))))
      position.setTitle(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionTitle')))
      position.setClientName(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionClientName')))
      position.setClientAddress(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionClientAddress')))
      position.setClientAccountNumber(self.getText(xmlPosition, self._properties.getProperty('bpPathPositionClientAccountNumber')))
      position.setDocument(document)
      position.setStatus(self.getStatus())
      self.saveDocument(position)
      
  def getStatus(self):
    return self._dictManager.findDictionaryInstance('DOCUMENT_STATUS', 'NEW')

  def parseDate(self, dateAsString):
    return SimpleDateFormat(self._properties.getProperty('dateFormat')).parse(dateAsString)

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