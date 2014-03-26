import os
import traceback
import shutil
import xml.sax
from base.Container import Container

class FileWatchdog(Container):
  _newXMLs = self._properties.getProperty("xmlNewXMLs")
  _processedXMLs = self._properties.getProperty("xmlProcessedXMLs")
  _nonXMLDir = self._properties.getProperty("xmlNonXML")
  _errorXMLs = self._properties.getProperty("xmlErrorXMLs")
  
  def moveFile(self, source, destination):
    self._logger.info('moving ' + source + ' to ' + destination)
    shutil.move(source, destination)

  def getFiles(self):
    self._logger.info('processing files in ' + self._newXMLs)
    return os.listdir(self._newXMLs)

  def isXML(self, file):
    try:
      xml.sax.parse(open(file, 'rb'), xml.sax.ContentHandler())
      self._logger.info('file ' + file + ' is an xml file')
      return True
    except:
      self._logger.info('file ' + file + ' is not an xml file')
      return False

  def readFile(self, fullPath):
    return ''.join(open(fullPath, 'r').readlines())

  def processXML(self, content):
    try:
      return XMLLoader().process(content)
    except:
      self._logger.error('Error in processing xml file: ' + content)
      self._logger.error(traceback.format_exc())

  def processFiles(self):
    files = self.getFiles()
    self._logger.info('found[%d][%s]' % (len(files), ','.join(files)))
    for file in files:
      self._logger.info('processing ' + file)
      fullPath = self._newXMLs + os.sep + file
      if self.isXML(fullPath):
        if self.processXML(self.readFile(fullPath)):
          self._logger.info('file ' + file + ' processed')
          self.moveFile(fullPath, self._processedXMLs + os.sep + file)
        else:
          self._logger.warn('There is something wrong with ' + file)
          self.moveFile(fullPath, self._errorXMLs + os.sep + file)
      else:
        self.moveFile(fullPath, self._nonXMLDir + os.sep + file)
    self._logger.info('all files processed')