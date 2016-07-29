import helpers
helpers.init(globals())

from structures.Counter import CounterManager
CounterManager().persist()