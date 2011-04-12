__all__ = [
        "Provider",
        "LBState",
        "LibcloudLBError",
        "LibcloudLBImmutableError",
        ]

from libcloud.common.types import LibcloudError

class LibcloudLBError(LibcloudError): pass

class LibcloudLBImmutableError(LibcloudLBError): pass

class Provider(object):
    RACKSPACE = 0
    GOGRID = 1

class LBState(object):
    """
    Standart states for a loadbalancer

    @cvar RUNNING: loadbalancer is running and ready to use
    @cvar UNKNOWN: loabalancer state is unknown
    """

    RUNNING = 0
    PENDING = 1
    UNKNOWN = 2
