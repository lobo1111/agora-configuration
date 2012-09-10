from com.healthmarketscience.jackcess import Database
from java.io import File
import md5

class MSAccessDataReader(Container):
    _logger = Logger([:_scriptId])
    _sqlInsertData = """
        INSERT INTO `%s`(%s) VALUES(%s);
    """
    _sqlFindMd5 = """
        SELECT md5 FROM `%s` WHERE `md5` = '%s'
    """

    def __init__(self):
        self._logger.info('loading external data')
        db = Database.open(File(properties.getProperty('msAccessDBPath')))
        for name in db.getTableNames():
            self.processTable(db.getTable(name))
        self._logger.info('external data loaded')

    def processTable(self, table):
        self._logger.info('processing table: %s' % table.getName())
        self.processTableData(table)
        self._logger.info('table processed')

    def processTableData(self, table):
        columns = table.getColumns()
        for row in table:
            self.processRow(table.getName(), row, columns)
            
    def processRow(self, tableName, row, columns):
        md5 = self.calculateMd5(row, columns)
        if not self.rowIsPresent(tableName, md5):
            self.insertRow(tableName, row, columns)
            
    def calculateMd5(self, row, columns):
        rawData = ''
        m = md5.new()
        for column in columns:
            m.update(row.get(column.getName()))
        return m.digest()
    
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
        return result + "`,`md5`"
    
    def getValuesString(self, row, columns):
        result = '"';
        for columns in columns:
            result += row.get(columns.getName()) + '","'
        return result + '","' + self.calculateMd5(row, columns) + '"'