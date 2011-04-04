import os

try:
    import json
except ImportError:
    import simplejson

from libcloud.common.base import Response
from libcloud.lb.base import LB, LBNode, LBDriver
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

    def create_balancer(self, **kwargs):
        name = kwargs['name']
        port = kwargs['port']
        nodes = kwargs['nodes']

        balancer_object = {"loadBalancer":
                {"name": name,
                    "port": port,
                    "protocol": "HTTP",
                    "virtualIps": [{"type": "PUBLIC"}],
                    "nodes": [{"address": node.ip,
                        "port": node.port,
                        "condition": "ENABLED"} for node in nodes],
                    }
                }

        resp = self.connection.request('/loadbalancers',
                method='POST',
                data=json.dumps(balancer_object))
        return self._to_balancer(resp.object["loadBalancer"])

    def destroy_balancer(self, balancer):
        uri = '/loadbalancers/%s' % (balancer.id)
        resp = self.connection.request(uri, method='DELETE')

        return resp.status == 202

    def balancer_detail(self, **kwargs):
        try:
            balancer_id = kwargs['balancer_id']
        except KeyError:
            balancer_id = kwargs['balancer'].id

        uri = '/loadbalancers/%s' % (balancer_id)
        resp = self.connection.request(uri)

        return self._to_balancer(resp.object["loadBalancer"])

    def balancer_detach_node(self, balancer, node):
        uri = '/loadbalancers/%s/nodes/%s' (balancer.id, node.id)
        resp = self.connection.request(uri, method='DELETE')

        return self.status == 202

    def balancer_list_nodes(self, balancer):
        uri = '/loadbalancers/%s/nodes' % (balancer.id)
        return self._to_nodes(
                self.connection.request(uri).object)

    def _to_balancers(self, object):
        return [ self._to_balancer(el) for el in object["loadBalancers"] ]

    def _to_balancer(self, el):
        lb = LB(id=el["id"],
                name=el["name"],
                state=el["status"],
                driver=self.connection.driver)
        return lb

    def _to_nodes(self, object):
        return [ self._to_node(el) for el in object["nodes"] ]

    def _to_node(self, el):
        lbnode = LBNode(id=el["id"],
                ip=el["address"],
                port=el["port"])
        return lbnode
