class Provider(object):
    RACKSPACE = 0

class LBState(object):
    """
    Standart states for a loadbalancer

    @cvar RUNNING: loadbalancer is running and ready to use
    @cvar UNKNOWN: loabalancer state is unknown
    """

    RUNNING = 0
    PENDING = 1
    UNKNOWN = 2
