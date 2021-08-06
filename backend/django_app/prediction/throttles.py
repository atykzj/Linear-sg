from rest_framework.throttling import UserRateThrottle

# Custom Throttle classes
class LimitedRateThrottle(UserRateThrottle):
    """Add in optional parameter to API requests to 'limited': '3/min' from mainapp/settings.py"""
    scope = 'limited'

class BurstRateThrottle(UserRateThrottle):
    """Add in optional parameter to API requests to 'burst': '10/min' from mainapp/settings.py"""
    scope = 'burst'