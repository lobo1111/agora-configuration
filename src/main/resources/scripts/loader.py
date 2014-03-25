import xml.etree.ElementTree as ET
import ConfigParser
import pymysql
import sys
import os

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
           
    def deleteAllSchedulers(self):
        sql = self._config.get('queries' ,'deleteAllSchedulers')
        cursor = self._connection.cursor()
        cursor.execute(sql)
        cursor.connection.commit()
        cursor.close()
    
    def insertScheduler(self, schedulerName, enabled, fireAt):
        sql = self._config.get('queries' ,'insetScheduler')
        cursor = self._connection.cursor()
        cursor.execute(sql % (schedulerName, enabled, fireAt))
        cursor.connection.commit()
        cursor.close()
        
class ScriptLoader:
    
    def __init__(self, db):
        self._config = ConfigManager()
        self._dbManager = DBManager(self._config, db)
        self._xml = ET.parse(self._config.get('paths', 'config')).getroot()
        
    def loadSchedulers(self):
        self._dbManager.deleteAllSchedulers()
        for scheduler in self._xml.findall('scheduler'):
            script = scheduler.find('script')
            enabled = scheduler.find('enabled')
            fireAt = scheduler.find('fireAt')
            self.saveScheduler(self.getText(script), self.getText(enabled), self.getText(fireAt))
            
    def saveScheduler(self, name, enabled, fireAt):
        print "Saving scheduler: " + name
        self._dbManager.insertScheduler(name, self.parseBoolean(enabled), fireAt)
        
    def getText(self, node):
        if node == None or node.text == None:
            return ""
        else:
            return node.text
        
    def parseBoolean(self, value):
        if value != None and value == 'true':
            return 1
        return 0;
    
class ScriptDeployer:
    
    def deployScripts(self, dest):
        self._config = ConfigManager()
        os.system("cp -Rf %s/* %s/" % (self._config.get('paths', 'scripts'), self._config.get('paths', dest)))
        
loader = ScriptLoader(sys.argv[1])
loader.loadSchedulers()
ScriptDeployer().deployScripts(sys.argv[2]) 