entityManager = None
svars = None
properties = None

def init(params):
    global entityManager, svars, properties, context
    entityManager = params['entityManager']
    svars = params['svars']
    properties = params['properties']