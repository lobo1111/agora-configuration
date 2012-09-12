from java.text import SimpleDateFormat
from pl.reaper.container.data import Address
from pl.reaper.container.data import Company
from pl.reaper.container.data import Person
from pl.reaper.container.data import Possession
from pl.reaper.container.data import Owner
from java.math import BigDecimal

class SyncPossessions(Sync):
    _logger = Logger([:_scriptId])
    _processed = 0
    _inserted = 0
    _updated = 0
    
    def sync(self):
        self._logger.info('synchronizing possessiona')
        possessions = self.loadData('SELECT w FROM Mieszkania w')
        for possession in possessions:
            self._processed += 1
            self._logger.info('processing possession %s' % possession.getMieszkanie())
            if self.possessionExists(possession):
                self._logger.info('possession exists, updating')
                self.possessionUpdate(possession)
                self._updated += 1
            else:
                self._logger.info('possession doesn\'t exists, inserting')
                self.possessionInsert(possession)
                self._inserted += 1
        self._logger.info('possession synchronized[processed:%d][inserted:%d][updated:%d]' % (self._processed, self._inserted, self._updated))

    def possessionExists(self, possession):
        return self.syncDataExists('sync_possession', 'access_possession_id', possession.getId())
    
    def possessionUpdate(self, possession):
        pass
    
    def possessionInsert(self, possession):
        pass