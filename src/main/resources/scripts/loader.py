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
        self._connection = pymysql.connect(host=config.get(db, 'host'), port=3306, user=config.get('db', 'user'), passwd=config.get('db', 'password'), db=config.get('db', 'db'))
        self._config = config
           
    def isScriptAvailable(self, scriptName):
        sql = self._config.get('queries' ,'selectScript')
        cursor = self._connection.cursor()
        cursor.execute(sql, (scriptName))
        results = cursor.fetchall()
        cursor.close()
        if len(results) > 0:
            return True
        return False
    
    def getScriptId(self, scriptName):
        sql = self._config.get('queries' ,'selectScript')
        cursor = self._connection.cursor()
        cursor.execute(sql, (scriptName))
        results = cursor.fetchall()
        cursor.close()
        if len(results) > 0: 
            return results[0][0]
        return -1
    
    def getGroupId(self, groupName):
        sql = self._config.get('queries' ,'selectGroup')
        cursor = self._connection.cursor()
        cursor.execute(sql, (groupName))
        results = cursor.fetchall()
        cursor.close()
        if len(results) > 0: 
            return results[0][0]
        return -1
    
    def updateScript(self, scriptName, source, onInit):
        sql = self._config.get('queries' ,'updateScript')
        cursor = self._connection.cursor()
        cursor.execute(sql, (source, onInit, scriptName))
        cursor.connection.commit()
        cursor.close()
    
    def insertScript(self, scriptName, source, onInit):
        sql = self._config.get('queries' ,'insertScript')
        cursor = self._connection.cursor()
        cursor.execute(sql, (scriptName, source, onInit))
        cursor.connection.commit()
        user_id = cursor.connection.insert_id()
        cursor.close()
        return user_id
    
    def deleteScriptScheduler(self, scriptId):
        sql = self._config.get('queries' ,'deleteScriptScheduler')
        cursor = self._connection.cursor()
        cursor.execute(sql % int(scriptId))
        cursor.connection.commit()
        cursor.close()
    
    def deleteScriptDependencies(self, scriptId):
        sql = self._config.get('queries' ,'deleteScriptDependencies')
        cursor = self._connection.cursor()
        cursor.execute(sql % int(scriptId))
        cursor.connection.commit()
        cursor.close()
    
    def deleteSecurityGroups(self, scriptId):
        sql = self._config.get('queries' ,'deleteSecurityGroups')
        cursor = self._connection.cursor()
        cursor.execute(sql % int(scriptId))
        cursor.connection.commit()
        cursor.close()
    
    def insertScriptScheduler(self, scriptId, schedulerName, enabled, fireAt):
        sql = self._config.get('queries' ,'insetScheduler')
        cursor = self._connection.cursor()
        cursor.execute(sql % (schedulerName, enabled, fireAt, int(scriptId)))
        cursor.connection.commit()
        cursor.close()
        
    def insertScriptDependency(self, scriptId, dependencyId):
        sql = self._config.get('queries' ,'insertDependency')
        cursor = self._connection.cursor()
        cursor.execute(sql % (int(scriptId), int(dependencyId)))
        cursor.connection.commit()
        cursor.close()
        
    def insertSecurityGroup(self, scriptId, groupId):
        sql = self._config.get('queries' ,'insertSecurityGroup')
        cursor = self._connection.cursor()
        cursor.execute(sql % (int(scriptId), int(groupId)))
        cursor.connection.commit()
        cursor.close()

class ScriptLoader:
    
    def __init__(self):
        self._config = ConfigManager()
        self._dbManager = DBManager(self._config)
        self._xml = ET.parse(self._config.get('paths', 'config')).getroot()
        
    def loadScripts(self):
        for script in self._xml.findall('script'):
            name = script.find('name')
            source = script.find('source')
            onInit = script.find('onInit')
            schedulerName = script.find('scheduler/name')
            schedulerEnabled = script.find('scheduler/enabled')
            schedulerFireAt = script.find('scheduler/fireAt')
            id = self.saveScript(self.getText(name), self.getText(source), self.getText(onInit))
            self.saveScheduler(id, self.getText(schedulerName), self.getText(schedulerEnabled), self.getText(schedulerFireAt))
            self.saveDependencies(id, script.findall('dependencies/scriptName'))
            self.saveSecurityGroups(id, script.findall('security/group'))
            
    def saveScript(self, name, source, onInit):
        print "Saving script: " + name
        if self._dbManager.isScriptAvailable(name):
            print "\tScript available, updating..."
            self._dbManager.updateScript(name, self.readFile(self._config.get('paths', 'scripts') + source), onInit)
            return self._dbManager.getScriptId(name)
        else:
            print "\tScript unavailable, inserting..."
            return self._dbManager.insertScript(name, self.readFile(self._config.get('paths', 'scripts') + source), onInit)
        
    def saveSecurityGroups(self, id, groups):
        self._dbManager.deleteSecurityGroups(id)
        for group in groups:
            groupName = self.getText(group)
            groupId = self._dbManager.getGroupId(groupName)
            print "\tAdding security group - [id:%d][name:%s]" % (groupId, groupName)
            self._dbManager.insertSecurityGroup(id, groupId)
        
    def saveDependencies(self, id, dependencies):
        self._dbManager.deleteScriptDependencies(id)
        for dependency in dependencies:
            dependencyName = self.getText(dependency)
            dependencyId = self._dbManager.getScriptId(dependencyName)
            print "\tAdding dependency - [id:%d][name:%s]" % (dependencyId, dependencyName)
            self._dbManager.insertScriptDependency(id, dependencyId)
                
    def saveScheduler(self, id, schedulerName, schedulerEnabled, schedulerFireAt):
        self._dbManager.deleteScriptScheduler(id)
        if schedulerName != "" and schedulerEnabled != "" and schedulerFireAt != "":
            print "\tSetting scheduler - [name:%s][enabled:%s][fireAt:%s]" % (schedulerName, schedulerEnabled, schedulerFireAt) 
            self._dbManager.insertScriptScheduler(id, schedulerName, self.parseBoolean(schedulerEnabled), schedulerFireAt)
        
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
    
loader = ScriptLoader(sys.argv[1])
loader.loadScripts()
            