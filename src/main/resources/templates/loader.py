import xml.etree.ElementTree as ET
import ConfigParser
import pymysql
import sys

class ConfigManager:
    _path = 'loader.config'
    
    def __init__(self):
        self._config = ConfigParser.ConfigParser()
        self._config.read('loader.config')
        
    def get(self, section, option):
        return self._config.get(section, option)

class DBManager:
    def __init__(self, config, db):
        self._connection = pymysql.connect(host=config.get('db', 'host'), port=3306, user=config.get('db', 'user'), passwd=config.get('db', 'password'), db=config.get('db', db))
        self._config = config
           
    def isTemplateAvailable(self, templateName):
        sql = self._config.get('queries' ,'selectTemplate')
        cursor = self._connection.cursor()
        cursor.execute(sql, (templateName))
        results = cursor.fetchall()
        cursor.close()
        if len(results) > 0:
            return True
        return False
    
    def getTemplateId(self, templateName):
        sql = self._config.get('queries' ,'selectTemplate')
        cursor = self._connection.cursor()
        cursor.execute(sql, (templateName))
        results = cursor.fetchall()
        cursor.close()
        if len(results) > 0: 
            return results[0][0]
        return -1
    
    def updateTemplate(self, templateName, content):
        sql = self._config.get('queries' ,'updateTemplate')
        cursor = self._connection.cursor()
        cursor.execute(sql, (content, templateName))
        cursor.connection.commit()
        cursor.close()
    
    def insertTemplate(self, templateName, content):
        sql = self._config.get('queries' ,'insertTemplate')
        cursor = self._connection.cursor()
        cursor.execute(sql, (templateName, content))
        cursor.connection.commit()
        user_id = cursor.connection.insert_id()
        cursor.close()
        return user_id
    
    def deleteTemplateVariables(self, templateId):
        sql = self._config.get('queries' ,'deleteTemplateVariables')
        cursor = self._connection.cursor()
        cursor.execute(sql % int(templateId))
        cursor.connection.commit()
        cursor.close()
    
    def insertTemplateVariable(self, templateId, variableName, data):
        sql = self._config.get('queries' ,'insetTemplateVariable')
        cursor = self._connection.cursor()
        cursor.execute(sql % (variableName, data, int(templateId)))
        cursor.connection.commit()
        cursor.close()
        
class TemplateLoader:
    
    def __init__(self, db):
        self._config = ConfigManager()
        self._dbManager = DBManager(self._config, db)
        self._xml = ET.parse(self._config.get('paths', 'config')).getroot()
        
    def loadTemplates(self):
        for template in self._xml.findall('template'):
            name = template.find('name')
            source = template.find('source')
            id = self.saveTemplate(self.getText(name), self.getText(source))
            self.saveVariables(id, template.findall('variables/var'))
            
    def saveTemplate(self, name, source):
        print "Saving template: " + name
        if self._dbManager.isTemplateAvailable(name):
            print "\tTemplate available, updating..."
            self._dbManager.updateTemplate(name, self.readFile(self._config.get('paths', 'templates') + source))
            return self._dbManager.getTemplateId(name)
        else:
            print "\tTemplate unavailable, inserting..."
            return self._dbManager.insertTemplate(name, self.readFile(self._config.get('paths', 'templates') + source))
        
    def saveVariables(self, id, variables):
        self._dbManager.deleteTemplateVariables(id)
        for var in variables:
            varName = self.getText(var.find('name'))
            varData = self.getText(var.find('data'))
            print "\tAdding template variable - [name:%s]" % (varName)
            self._dbManager.insertTemplateVariable(id, varName, varData)
                
    def getText(self, node):
        if node == None or node.text == None:
            return ""
        else:
            return node.text
        
    def parseBoolean(self, value):
        if value != None and value == 'true':
            return 1
        return 0;
        
    def readFile(self, fullPath):
        return ''.join(open(fullPath, 'r').readlines())
    
loader = TemplateLoader(sys.argv[1])
loader.loadTemplates()
            