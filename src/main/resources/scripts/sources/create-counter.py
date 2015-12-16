import helpers
helpers.init(globals())

from entities.Counter import CounterManager
counterManager = CounterManager()
counterManager.create()