from com.healthmarketscience.jackcess import Database;
from java.io import File

class MSAccessReader(Container):
    _logger = Logger([:_scriptId])
    _sqlCreateTable = """
        CREATE TABLE `%s` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci AUTO_INCREMENT=1;
        """
    _sqlAddColumn = """
        ALTER TABLE `%s` ADD COLUMN `%s` VARCHAR(256);
    """
    _sqlInsert = """
        INSERT INTO `%s`(`%s`) VALUES("%s");
    """
    _sqlSelectFromTable = """
        SELECT * FROM `%s`
    """

    def __init__(self):
        self._logger.info('loading external data')
        db = Database.open(File(properties.getProperty('msAccessDBPath')))
        for name in db.getTableNames():
            self.processTable(db.getTable(name))
        self._logger.info('external data loaded')

    def processTable(self, table):
        self._logger.info('processing table: %s' % table.getName())
        self.processTableStructure(table)
        self.insertData(table)
        self._logger.info('table processed')

    def processTableStructure(self, table):
        self.createTableIfNotExists(table.getName())
        columns = table.getColumns()
        for column in columns:
            self.addColumn(table.getName(), column.getName())

    def createTableIfNotExists(self, name):
        if not self.tableExists(name):
            self._logger.info('creating table %s' % name)
            sql = (self._sqlCreateTable % (name))
            oldEntityManager.createNativeQuery(sql).executeUpdate()
        else:
            self._logger.info('table already exists')
            
    def tableExists(self, name):
        try:
            oldEntityManager.createNativeQuery(sql).getResultList()
            return True
        except:
            return False

    def addColumn(self, tableName, columnName):
        try:
            self._logger.info('adding column: %s' % name)
            sql = (self._sqlAddColumn % (tableName, columnName))
            oldEntityManager.createNativeQuery(sql).executeUpdate()
        except:
            self._logger.info('column already exists')

    def insertData(self, table):
        pass
