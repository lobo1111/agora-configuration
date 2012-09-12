class SyncAccessToDb(Container):
    _logger = Logger([:_scriptId])
        
    def __init__(self):
        self._logger.info('synchronizing databses...')
        SyncCommunities().sync()
        SyncPeople().sync()
        SyncCompanies().sync()
        #SyncPossessions().sync()
        self._logger.info('synchronization complete')