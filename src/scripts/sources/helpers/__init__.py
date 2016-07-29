entityManager = None
svars = None
context = None

def init(params):
    global entityManager, svars, context
    entityManager = params['entityManager']
    svars = params['svars']
    context = params['context']