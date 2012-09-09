from com.healthmarketscience.jackcess import Database;
from java.io import File

class MSAccessReader(Container):
    _sqlCreateTable = """
        CREATE TABLE `{0}` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (`id`),
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci AUTO_INCREMENT=1 ;
        """
    _sqlAddColumn = """
        ALTER TABLE `{0}` ADD COLUMN `{1}` VARCHAR(1024);
    """
    _sqlInsert = """
        INSERT INTO `{0}`(`{1}`) VALUES("{2}");
    """
    
    def __init__(self):
        self.clearDatabase()
        tables = Database.open(File(properties.getProperty('msAccessDBPath'))).getTableNames() 
        for table in tables:
            self.processTable(table)

    def processTable(self, table):
        self.processTableStructure(table)
        self.processTableData(table)

    def clearDatabase(self):
        pass

    def processTableStructure(self, table):
        self.createTable(table.getName())
        columns = table.getColumns()
        for column in columns:
            self.addColumn(column.getName())

    def createTable(self, name):
        oldEntityManager.createNativeQuery(self._sqlCreateTable % name).executeUpdate()

    def addColumn(self, name):
        pass
