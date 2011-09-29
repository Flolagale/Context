import time
#import android
#droid = android.Android()

class RuleManager:
    """The context class provides definitions of rules
    and events which are actions to be realized in specific
    contexts of time and location. """
    def __init__(self):
        self._rules = []
        self._events = []

    def addRule(self, rule):
        self._rules.append(rule)

    def followRules(self):
        for rule in self._rules:
            performAction = True
            contexts = rule['context']
            # Compare current context and rule context:
            if 'time' in contexts:
                if not (time.localtime().tm_hour == contexts['time'][0] and time.localtime().tm_min == contexts['time'][1]):
                    performAction = False

            currentLocation = 'ici'
            if 'location' in contexts:
                if not currentLocation == contexts['location']:
                    performAction = False

            if performAction:
                print 'Perform action.'
                rule['action']()
            else:
                print 'Not doing anything.'
                
# ---------------------------
def toast():
    #droid.makeToast('salut')
    #droid.speak('salut')
    print 'Toasting.'
    

# ---------------------------
ruleMgr = RuleManager()
ruleMgr.addRule({
    'context': {
        'time': (15,33),
        'location': 'ici'
    },
    'action': toast
})

ruleMgr.addRule({
    'context': {
        'time': (14,22),
        'location': 'travail'
    },
    'action': toast
})

ruleMgr.followRules()

