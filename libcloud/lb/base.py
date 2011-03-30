from libcloud.common.base import ConnectionKey

class LB(object):

    def __init__(self, id, name, state):
        self.id = str(id) if id else None
        self.name = name
        self.state = state

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
