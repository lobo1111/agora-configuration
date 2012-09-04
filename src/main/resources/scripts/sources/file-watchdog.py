import os
import shutil
import xml.sax

class FileWatchdog(Container):
  _newFiles = properties.getProperty("emailAttachmentsDir")
  _processedXMLs = properties.getProperty("xmlProcessedXMLs")
  _nonXMLDir = properties.getProperty("xmlNonXML")
  _errorXMLs = properties.getProperty("xmlErrorXMLs")
  _logger = Logger([:_scriptId])
  
  def moveFile(self, source, destination):
    self._logger.info('moving ' + source + ' to ' + destination)
    shutil.move(source, destination)

  def getFiles(self):
    return os.listdir(self._newFiles)

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

  def processFiles(self):
    files = self.getFiles()
    self._logger.info('processing new files - ' + str(len(files)))
    for file in files:
      fullPath = self._newFiles + os.sep + file
      self._logger.info('processing ' + file)
      if self.isXML(fullPath):
        if self.processXML(self.readFile(fullPath)):
          self._logger.info('file ' + file + ' processed')
          self.moveFile(fullPath, self._processedXMLs + os.sep + file)
        else:
          self._logger.warning('There is something wrong with ' + file)
          self.moveFile(fullPath, self._errorXMLs + os.sep + file)
      else:
        self.moveFile(fullPath, self._nonXMLDir + os.sep + file)
    self._logger.info('all files processed')