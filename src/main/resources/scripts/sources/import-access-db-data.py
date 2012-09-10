from com.healthmarketscience.jackcess import Database
from java.io import File
import hashlib

class MSAccessDataReader(Container):
    _logger = Logger([:_scriptId])
    _sqlInsertData = """
        INSERT INTO `%s`(%s) VALUES(%s);
    """
    _sqlFindMd5 = """
        SELECT md5 FROM `%s` WHERE `md5` = '%s'
    """
    _processed = 0
    _inserted = 0
    _omitted = 0

    def __init__(self):
        self._logger.info('loading external data')
        db = Database.open(File(properties.getProperty('msAccessDBPath')))
        for name in db.getTableNames():
            self.processTable(db.getTable(name))
        self._logger.info('external data loaded')

    def processTable(self, table):
        self._logger.info('processing table: %s' % table.getName())
        self.processTableData(table)
        self._logger.info(('table processed[processed:%d][inserted:%d][omitted:%d]' % (self._processed, self._inserted, self._omitted)))

    def processTableData(self, table):
        columns = table.getColumns()
        for row in table:
            self.processRow(table.getName(), row, columns)
            
    def processRow(self, tableName, row, columns):
        self._processed += 1
        md5 = self.calculateMd5(row, columns)
        if not self.rowIsPresent(tableName, md5):
            self._inserted += 1
            self.insertRow(tableName, row, columns)
        else:
            self._omitted += 1
            
    def calculateMd5(self, row, columns):
        rawData = ''
        for column in columns:
            rawData += str((row.get(column.getName())).decode('cp1250'))
        return hashlib.md5(rawData).hexdigest()
    
    def rowIsPresent(self, tableName, md5):
        try:
            sql = self._sqlFindMd5 % (tableName, md5)
            oldEntityManager.createNativeQuery(sql).getSingleResult()
            return True
        except:
            return False
        
    def insertRow(self, tableName, row, columns):
        columnsString = self.getColumnsString(columns)
        valuesString = self.getValuesString(row, columns)
        sql = self._sqlInsertData % (tableName, columnsString, valuesString)
        oldEntityManager.createNativeQuery(sql).executeUpdate()

    def getColumnsString(self, columns):
        result = '`';
        for column in columns:
            result += column.getName() + "`,`"
        return result + "md5`"
    
    def getValuesString(self, row, columns):
        result = '"';
        for column in columns:
            result += str(row.get(column.getName())) + '","'
        return result + str(self.calculateMd5(row, columns)) + '"'