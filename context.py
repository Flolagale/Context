import time
import math
import android

# ---------------------------
class RuleManager:
    """
    The RuleManager class provides services to handle the user defined rules
    which are actions to be realized in specific contexts of time and location.
    """
    def __init__(self):
        self._rules = []

    def addRule(self, rule):
        self._rules.append(rule)
        print self._rules

    def followRules(self):
        global androidHelper
        
        for rule in self._rules:
            performAction = True
            contexts = rule['context']
            
            # Compare current context and rule context:
            if 'time' in contexts:
                if not (time.localtime().tm_hour == contexts['time'][0] and time.localtime().tm_min == contexts['time'][1]):
                    performAction = False

            if 'location' in contexts:
                currentLocation = androidHelper.getCurrentLocation()
                if not self.areSameLocations(contexts['location'], currentLocation):
                    performAction = False

            if performAction:
                print 'Perform action.'
                rule['action']()
            else:
                print 'Not doing anything.'

    def areSameLocations(self, location1, location2):
        """
        using the spherical law of cosines from 
        http://www.movable-type.co.uk/scripts/latlong.html
        this law gives the distance in kilometers.
        """
        R = 6371
        lat1 = math.radians(location1['latitude'])
        lat2 = math.radians(location2['latitude'])
        lon1 = math.radians(location1['longitude'])
        lon2 = math.radians(location2['longitude'])
        dist = math.acos(math.sin(lat1)*math.sin(lat2) +
                          (math.cos(lat1)*math.cos(lat2) *
                           math.cos(lon2-lon1))) * R
        tolerance = 2
        return (dist < 2)

# ---------------------------
class AndroidHelper:
    """
    The AndroidHelper class provides some helping functions
    for the Android Facade API.
    """
    def __init__(self):
        self._droid = android.Android()

    def getCurrentLocation(self):
        self._droid.startLocating()
        time.sleep(2)
        loc = self._droid.readLocation()
        while len(loc.result) == 0:
            print loc
            time.sleep(1)
            loc = self._droid.readLocation()

        self._droid.stopLocating()

        print loc.result['network']['latitude']
        print loc.result['network']['longitude']
        
        return {
            'latitude': loc.result['network']['latitude'],
            'longitude': loc.result['network']['longitude']}

    def makeToast(self, message):
        self._droid.makeToast(message)
        print 'Toasting.'

# ---------------------------
# Available actions:
def toast():
    androidHelper = AndroidHelper()
    androidHelper.makeToast('toasting')

# ---------------------------
androidHelper = AndroidHelper()
ruleMgr = RuleManager()

ruleMgr.addRule({
    'context': {
        'time': (15,26),
        'location': {
            'latitude': 45.7797498,
            'longitude':  4.8770637
            }
        },
        'action': toast
})

ruleMgr.addRule({
    'context': {
        'time': (14,22),
    },
    'action': toast
})

ruleMgr.followRules()

