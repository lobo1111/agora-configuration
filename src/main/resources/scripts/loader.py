import xml.etree.ElementTree as ET

class ScriptLoader:
    _xmlPath = '/opt/builder/src/src/main/resources/scripts/main.xml'
    _Scriptspath = '/opt/builder/src/src/main/resources/scripts/sources'
    
    def __init__(self):
        self._xml = ET.parse(self._xmlPath).getroot()
        
    def loadScripts(self):
        for script in self._xml.findall('/cripts/script'):
            name = script.find('name')
            source = script.find('source')
            onInit = script.find('onInit')
            schedulerName = script.find('scheduler/name')
            schedulerEnabled = script.find('scheduler/enabled')
            schedulerFireAt = script.find('scheduler/fireAt')
            id = saveScript(name, source, onInit, schedulerName, schedulerEnabled, schedulerFireAt)
            saveDependencies(id, script.findall('dependencies'))
            
    def saveScript(self, name, source, onInit, schedulerName, schedulerEnabled, schedulerFireAt):
        print name
        print source
        print onInit
        print schedulerName
        print schedulerEnabled
        print schedulerFireAt
        
    def saveDependencies(self, dependencies):
        print dependencies
        
loader = ScriptLoader()
loader.loadScripts()
            