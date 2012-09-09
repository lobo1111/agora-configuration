from com.healthmarketscience.jackcess import Database;
from java.io import File

class MSAccessReader(Container):
    _sqlCreateTable = """
        CREATE TABLE `%s` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci AUTO_INCREMENT=1;
        """
    _sqlAddColumn = """
        ALTER TABLE `%s` ADD COLUMN `%s` VARCHAR(512);
    """
    _sqlInsert = """
        INSERT INTO `%s`(`%s`) VALUES("%s");
    """

    def __init__(self):
        self.clearDatabase()
        db = Database.open(File(properties.getProperty('msAccessDBPath')))
        for name in db.getTableNames():
            self.processTable(db.getTable(name))

    def processTable(self, table):
        self.processTableStructure(table)

    def clearDatabase(self):
        pass

    def processTableStructure(self, table):
        self.createTable(table.getName())
        columns = table.getColumns()
        for column in columns:
            self.addColumn(table.getName(), column.getName())
            self.insertData(table, column.getName())

    def createTable(self, name):
        oldEntityManager.createNativeQuery((self._sqlCreateTable % (name))).executeUpdate()

    def addColumn(self, tableName, columnName):
        oldEntityManager.createNativeQuery((self._sqlAddColumn % (tableName, columnName))).executeUpdate()

    def insertData(self, table, columnName):
        for row in table:
            oldEntityManager.createNativeQuery((self._sqlInsert % (table.getName, columnName, row.get(columnName))).executeUpdate()
