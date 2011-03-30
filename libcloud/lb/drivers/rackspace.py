import os

try:
    import json
except ImportError:
    import simplejson

from libcloud.common.base import Response
from libcloud.lb.base import LB, LBDriver
from libcloud.lb.types import Provider
from libcloud.common.rackspace import (AUTH_HOST_US,
        RackspaceBaseConnection)

class RackspaceResponse(Response):

    def success(self):
        return 200 <= int(self.status) <= 299

    def parse_body(self):
        if not self.body:
            return None
        else:
            return json.loads(self.body)

class RackspaceConnection(RackspaceBaseConnection):
    responseCls = RackspaceResponse
    auth_host = AUTH_HOST_US
    _url_key = "lb_url"

    def __init__(self, user_id, key, secure=True):
        super(RackspaceConnection, self).__init__(user_id, key, secure)
        self.api_version = 'v1.0'
        self.accept_format = 'application/json'

    def request(self, action, params=None, data='', headers=None, method='GET'):
        if not headers:
            headers = {}
        if not params:
            params = {}
        if self.lb_url:
            action = self.lb_url + action
        if method in ('POST', 'PUT'):
            headers['Content-Type'] = 'application/json'
        if method == 'GET':
            params['cache-busing'] = os.urandom(8).encode('hex')
        return super(RackspaceConnection, self).request(action=action,
                params=params, data=data, method=method, headers=headers)


class RackspaceLBDriver(LBDriver):
    connectionCls = RackspaceConnection
    type = Provider.RACKSPACE
    api_name = 'rackspace_lb'
    name = 'Rackspace LB'

    def list_balancers(self):
        return self._to_balancers(
                self.connection.request('/loadbalancers').object)

    def _to_balancers(self, object):
        return [ self._to_balancer(el) for el in object["loadBalancers"] ]

    def _to_balancer(self, el):
        lb = LB(id=el["id"],
                name=el["name"],
                state=el["status"])
        return lb
