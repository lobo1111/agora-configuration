from com.healthmarketscience.jackcess import Database;
from java.io import File

class MSAccessReader(Container):
    
    def __init__(self):
        print Database.open(File(properties.getProperty('msAccessDBPath'))).getTableNames() 