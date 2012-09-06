import xml.etree.ElementTree as ET
import pymysql


class ScriptLoader:
    _xmlPath = '/opt/builder/src/src/main/resources/scripts/main.xml'
    _Scriptspath = '/opt/builder/src/src/main/resources/scripts/sources'
    
    def __init__(self):
        self._xml = ET.parse(self._xmlPath).getroot()
        self._connection = pymysql.connect(host='172.16.1.5', port=3306, user='agora', passwd='tomasz.12', db='agora_erp')
        
    def loadScripts(self):
        for script in self._xml.findall('script'):
            name = script.find('name')
            source = script.find('source')
            onInit = script.find('onInit')
            schedulerName = script.find('scheduler/name')
            schedulerEnabled = script.find('scheduler/enabled')
            schedulerFireAt = script.find('scheduler/fireAt')
            id = self.saveScript(self.getText(name), self.getText(source), self.getText(onInit))
            print id
            self.saveScheduler(id, self.getText(schedulerName), self.getText(schedulerEnabled), self.getText(schedulerFireAt))
            self.saveDependencies(id, script.findall('dependencies'))
            
    def saveScript(self, name, source, onInit):
        sql = """INSERT INTO script (name, script, on_init) VALUES (%s, %s, %s)"""
        cursor = self._connection.cursor()
        cursor.execute(sql, (name, source, onInit))
        cursor.connection.commit()
        user_id = cursor.connection.insert_id()
        cursor.close()
        return user_id
        
    def saveDependencies(self, id, dependencies):
        print dependencies
                
    def saveScheduler(self, id, schedulerName, schedulerEnabled, schedulerFireAt):
        print schedulerName
        
    def getText(self, node):
        if node == None or node.text == None:
            return ""
        else:
            return node.text
        
loader = ScriptLoader()
loader.loadScripts()
            