from libcloud.common.base import ConnectionKey

class LBNode(object):

    def __init__(self, id, ip, port):
        self.id = str(id) if id else None
        self.ip = ip
        self.port = port

    def __repr__(self):
        return ('<LBNode: id=%s, address=%s:%s>' % (self.id,
            self.ip, self.port))


class LB(object):

    def __init__(self, id, name, state, driver):
        self.id = str(id) if id else None
        self.name = name
        self.state = state
        self.driver = driver

    def attach_node(self, node):
        return self.driver.balancer_attach_node(self, node)

    def detach_node(self, node):
        return self.driver.balancer_detach_node(self, node)

    def list_nodes(self):
        return self.driver.balancer_list_nodes(self)

    def __repr__(self):
        return ('<LB: id=%s, name=%s, state=%s>' % (self.id,
                self.name, self.state))


class LBDriver(object):
    connectionCls = ConnectionKey

    def __init__(self, key, secret=None, secure=True):
        self.key = key
        self.secret = secret
        args = [self.key]

        if self.secret is not None:
            args.append(self.secret)

        args.append(secure)

        self.connection = self.connectionCls(*args)
        self.connection.driver = self
        self.connection.connect()

    def list_balancers(self):
        raise NotImplementedError, \
                'list_balancers not implemented for this driver'

    def create_balancer(self, **kwargs):
        raise NotImplementedError, \
                'create_balancer not implemented for this driver'

    def destroy_balancer(self, balancer):
        raise NotImplementedError, \
                'destroy_balancer not implemented for this driver'

    def balancer_detail(self, **kwargs):
        raise NotImplementedError, \
                'balancer_detail not implemented for this driver'

    def balancer_attach_node(self, balancer, node):
        raise NotImplementedError, \
                'balancer_attach_node not implemented for this driver'

    def balancer_detach_node(self, balancer, node):
        raise NotImplementedError, \
                'balancer_detach_node not implemented for this driver'

    def balancer_list_nodes(self, balancer):
        raise NotImplementedError, \
                'balancer_list_nodes not implemented for this driver'
