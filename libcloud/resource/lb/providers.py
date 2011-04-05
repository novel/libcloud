from libcloud.utils import get_driver as get_provider_driver
from libcloud.lb.types import Provider

__all__ = [
        "Provider",
        "DRIVERS",
        "get_driver",
        ]

DRIVERS = {
        Provider.RACKSPACE:
            ('libcloud.lb.drivers.rackspace', 'RackspaceLBDriver'),
}

def get_driver(provider):
    return get_provider_driver(DRIVERS, provider)
